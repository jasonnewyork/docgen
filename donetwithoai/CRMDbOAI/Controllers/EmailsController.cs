using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using CRMDbOAI.Models;
using CRMDbOAI.Services;

namespace CRMDbOAI.Controllers
{
    public class EmailsController : Controller
    {
        private readonly IEmailService _emailService;
        private readonly ICustomerService _customerService;

        public EmailsController(IEmailService emailService, ICustomerService customerService)
        {
            _emailService = emailService;
            _customerService = customerService;
        }

        // GET: Emails/Create
        public async Task<IActionResult> Create()
        {
            var customers = await _customerService.GetAllAsync();
            ViewBag.Customers = customers;
            return View();
        }

        // POST: Emails/Preview
        [HttpPost]
        public async Task<IActionResult> Preview(List<int> selectedCustomerIds, string templateText)
        {
            var allCustomers = await _customerService.GetAllAsync();
            var selectedCustomers = new List<customer>();
            foreach (var id in selectedCustomerIds)
            {
                var customer = await _customerService.GetByIdAsync(id);
                if (customer != null)
                    selectedCustomers.Add(customer);
            }
            var emails = await _emailService.GenerateEmailsAsync(selectedCustomers, templateText);
            ViewBag.TemplateText = templateText;
            return View(emails);
        }

        // POST: Emails/Send
        [HttpPost]
        public async Task<IActionResult> Send(List<GeneratedEmail> emails)
        {
            await _emailService.SendEmailsAsync(emails);
            return RedirectToAction("Sent");
        }

        // GET: Emails/Sent
        public IActionResult Sent()
        {
            return View();
        }
    }
}
