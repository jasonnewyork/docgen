using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using MyCRM.Services;
using MyCRM.Models.DTOs;
using System.Security.Claims;

namespace MyCRM.Controllers
{
    // [Authorize] // Temporarily disabled for testing without authentication
    public class EmailController : Controller
    {
        private readonly EmailService _emailService;
        private readonly CustomerService _customerService;
        private readonly ILogger<EmailController> _logger;

        public EmailController(EmailService emailService, CustomerService customerService, ILogger<EmailController> logger)
        {
            _emailService = emailService;
            _customerService = customerService;
            _logger = logger;
        }

        // GET: Email
        public async Task<IActionResult> Index(int page = 1, int pageSize = 20, string search = "", DateTime? startDate = null, DateTime? endDate = null)
        {
            try
            {
                var emailLogs = await _emailService.GetEmailLogsAsync(page, pageSize, search, startDate, endDate);
                ViewBag.Search = search;
                ViewBag.StartDate = startDate?.ToString("yyyy-MM-dd");
                ViewBag.EndDate = endDate?.ToString("yyyy-MM-dd");
                ViewBag.PageSize = pageSize;
                return View(emailLogs);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving email logs");
                TempData["Error"] = "An error occurred while retrieving email logs.";
                return View(new PagedResult<EmailLogDto>());
            }
        }

        // GET: Email/Details/5
        public async Task<IActionResult> Details(int id)
        {
            try
            {
                var emailLog = await _emailService.GetEmailLogByIdAsync(id);
                if (emailLog == null)
                {
                    return NotFound();
                }
                return View(emailLog);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving email log {EmailLogId}", id);
                TempData["Error"] = "An error occurred while retrieving the email log.";
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: Email/Compose
        [Authorize(Roles = "Administrator,PowerUser,CustomerManager")]
        public async Task<IActionResult> Compose(int? customerId = null)
        {
            try
            {
                var model = new ComposeEmailDto();
                
                if (customerId.HasValue)
                {
                    var customer = await _customerService.GetCustomerByIdAsync(customerId.Value);
                    if (customer != null)
                    {
                        model.Recipients = new List<string> { customer.Email };
                        model.CustomerIds = new List<int> { customer.Id };
                        ViewBag.Customer = customer;
                    }
                }

                // Get available templates
                var templates = await _emailService.GetEmailTemplatesAsync();
                ViewBag.Templates = templates;

                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading compose email page");
                TempData["Error"] = "An error occurred while loading the compose page.";
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Email/Compose
        [HttpPost]
        [ValidateAntiForgeryToken]
        [Authorize(Roles = "Administrator,PowerUser,CustomerManager")]
        public async Task<IActionResult> Compose(ComposeEmailDto dto)
        {
            if (!ModelState.IsValid)
            {
                var templates = await _emailService.GetEmailTemplatesAsync();
                ViewBag.Templates = templates;
                return View(dto);
            }

            try
            {
                var sentBy = User.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? "System";
                var result = await _emailService.SendEmailAsync(dto, sentBy);
                
                if (result)
                {
                    TempData["Success"] = "Email sent successfully.";
                    return RedirectToAction(nameof(Index));
                }
                else
                {
                    ModelState.AddModelError("", "Failed to send email.");
                    var templates = await _emailService.GetEmailTemplatesAsync();
                    ViewBag.Templates = templates;
                    return View(dto);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending email");
                ModelState.AddModelError("", "An error occurred while sending the email.");
                var templates = await _emailService.GetEmailTemplatesAsync();
                ViewBag.Templates = templates;
                return View(dto);
            }
        }

        // GET: Email/GenerateAI
        [Authorize(Roles = "Administrator,PowerUser,CustomerManager")]
        public async Task<IActionResult> GenerateAI(int? customerId = null)
        {
            try
            {
                var model = new GenerateAIEmailDto();
                
                if (customerId.HasValue)
                {
                    var customer = await _customerService.GetCustomerByIdAsync(customerId.Value);
                    if (customer != null)
                    {
                        model.CustomerId = customer.Id;
                        ViewBag.Customer = customer;
                    }
                }

                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading AI email generation page");
                TempData["Error"] = "An error occurred while loading the AI generation page.";
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Email/GenerateAI
        [HttpPost]
        [ValidateAntiForgeryToken]
        [Authorize(Roles = "Administrator,PowerUser,CustomerManager")]
        public async Task<IActionResult> GenerateAI(GenerateAIEmailDto dto)
        {
            if (!ModelState.IsValid)
            {
                if (dto.CustomerId.HasValue)
                {
                    var customer = await _customerService.GetCustomerByIdAsync(dto.CustomerId.Value);
                    ViewBag.Customer = customer;
                }
                return View(dto);
            }

            try
            {
                var content = await _emailService.GenerateAIEmailAsync(dto);
                
                // Redirect to compose with generated content
                var composeModel = new ComposeEmailDto
                {
                    Subject = "AI Generated Email",
                    Content = content,
                    CustomerIds = dto.CustomerId.HasValue ? new List<int> { dto.CustomerId.Value } : new List<int>()
                };

                if (dto.CustomerId.HasValue)
                {
                    var customer = await _customerService.GetCustomerByIdAsync(dto.CustomerId.Value);
                    if (customer != null)
                    {
                        composeModel.Recipients = new List<string> { customer.Email };
                    }
                }

                TempData["Success"] = "AI email content generated successfully.";
                TempData["GeneratedEmail"] = Newtonsoft.Json.JsonConvert.SerializeObject(composeModel);
                return RedirectToAction(nameof(Compose));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating AI email");
                ModelState.AddModelError("", "An error occurred while generating the AI email.");
                if (dto.CustomerId.HasValue)
                {
                    var customer = await _customerService.GetCustomerByIdAsync(dto.CustomerId.Value);
                    ViewBag.Customer = customer;
                }
                return View(dto);
            }
        }

        // GET: Email/BulkEmail
        [Authorize(Roles = "Administrator,PowerUser")]
        public async Task<IActionResult> BulkEmail()
        {
            try
            {
                var model = new BulkEmailDto();
                var templates = await _emailService.GetEmailTemplatesAsync();
                ViewBag.Templates = templates;
                return View(model);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading bulk email page");
                TempData["Error"] = "An error occurred while loading the bulk email page.";
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Email/BulkEmail
        [HttpPost]
        [ValidateAntiForgeryToken]
        [Authorize(Roles = "Administrator,PowerUser")]
        public async Task<IActionResult> BulkEmail(BulkEmailDto dto)
        {
            if (!ModelState.IsValid)
            {
                var templates = await _emailService.GetEmailTemplatesAsync();
                ViewBag.Templates = templates;
                return View(dto);
            }

            try
            {
                var sentBy = User.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? "System";
                var result = await _emailService.SendBulkEmailAsync(dto, sentBy);
                
                if (result)
                {
                    TempData["Success"] = "Bulk email sent successfully.";
                    return RedirectToAction(nameof(Index));
                }
                else
                {
                    ModelState.AddModelError("", "Failed to send bulk email.");
                    var templates = await _emailService.GetEmailTemplatesAsync();
                    ViewBag.Templates = templates;
                    return View(dto);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending bulk email");
                ModelState.AddModelError("", "An error occurred while sending the bulk email.");
                var templates = await _emailService.GetEmailTemplatesAsync();
                ViewBag.Templates = templates;
                return View(dto);
            }
        }

        // GET: Email/Templates
        [Authorize(Roles = "Administrator,PowerUser")]
        public async Task<IActionResult> Templates()
        {
            try
            {
                var templates = await _emailService.GetEmailTemplatesAsync();
                return View(templates);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving email templates");
                TempData["Error"] = "An error occurred while retrieving email templates.";
                return View(new List<EmailTemplateDto>());
            }
        }

        // POST: Email/SaveTemplate
        [HttpPost]
        [ValidateAntiForgeryToken]
        [Authorize(Roles = "Administrator,PowerUser")]
        public async Task<IActionResult> SaveTemplate(EmailTemplateDto dto)
        {
            if (!ModelState.IsValid)
            {
                return Json(new { success = false, message = "Invalid template data." });
            }

            try
            {
                var createdBy = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
                await _emailService.SaveEmailTemplateAsync(dto);
                return Json(new { success = true, message = "Template saved successfully." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error saving email template");
                return Json(new { success = false, message = "An error occurred while saving the template." });
            }
        }

        // POST: Email/DeleteTemplate
        [HttpPost]
        [ValidateAntiForgeryToken]
        [Authorize(Roles = "Administrator,PowerUser")]
        public async Task<IActionResult> DeleteTemplate(int id)
        {
            try
            {
                await _emailService.DeleteEmailTemplateAsync(id);
                return Json(new { success = true, message = "Template deleted successfully." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting email template {TemplateId}", id);
                return Json(new { success = false, message = "An error occurred while deleting the template." });
            }
        }

        // GET: Email/Analytics
        [Authorize(Roles = "Administrator,PowerUser")]
        public async Task<IActionResult> Analytics(DateTime? startDate = null, DateTime? endDate = null)
        {
            try
            {
                var analytics = await _emailService.GetEmailAnalyticsAsync();
                ViewBag.StartDate = startDate?.ToString("yyyy-MM-dd");
                ViewBag.EndDate = endDate?.ToString("yyyy-MM-dd");
                return View(analytics);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving email analytics");
                TempData["Error"] = "An error occurred while retrieving email analytics.";
                return View(new EmailAnalyticsDto());
            }
        }

        // GET: Email/Export
        [Authorize(Roles = "Administrator,PowerUser")]
        public async Task<IActionResult> Export(DateTime? startDate = null, DateTime? endDate = null, string format = "csv")
        {
            try
            {
                var exportData = await _emailService.ExportEmailLogsAsync(format);
                var fileName = $"email_logs_{DateTime.Now:yyyyMMdd_HHmmss}.{format}";
                var contentType = format.ToLower() == "csv" ? "text/csv" : "application/json";
                
                return File(exportData, contentType, fileName);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting email logs");
                TempData["Error"] = "An error occurred while exporting email logs.";
                return RedirectToAction(nameof(Index));
            }
        }
    }
}
