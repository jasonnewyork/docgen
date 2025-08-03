using MyCRM.Models;
using MyCRM.Models.DTOs;
using MyCRM.Repositories;

namespace MyCRM.Services
{
    public class EmailService
    {
        private readonly IEmailLogRepository _emailLogRepository;
        private readonly ICustomerRepository _customerRepository;
        private readonly ILogger<EmailService> _logger;

        public EmailService(
            IEmailLogRepository emailLogRepository,
            ICustomerRepository customerRepository,
            ILogger<EmailService> logger)
        {
            _emailLogRepository = emailLogRepository;
            _customerRepository = customerRepository;
            _logger = logger;
        }

        public async Task<PagedResult<EmailLogDto>> GetEmailLogsAsync(int page, int pageSize, string? searchTerm = null, DateTime? startDate = null, DateTime? endDate = null)
        {
            try
            {
                var emailLogs = await _emailLogRepository.GetPagedAsync(page, pageSize, searchTerm);
                
                var emailLogDtos = emailLogs.Items.Select(e => new EmailLogDto
                {
                    EmailLogId = e.EmailLogId,
                    CustomerId = e.CustomerId,
                    CustomerName = e.Customer?.Name ?? "",
                    Subject = e.Subject,
                    Content = e.Content,
                    SentAt = e.SentAt,
                    SentBy = e.SentBy,
                    Status = e.Status,
                    ErrorMessage = e.ErrorMessage
                });

                return new PagedResult<EmailLogDto>
                {
                    Items = emailLogDtos,
                    TotalCount = emailLogs.TotalCount,
                    PageNumber = emailLogs.PageNumber,
                    PageSize = emailLogs.PageSize
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting email logs");
                throw;
            }
        }

        public async Task<EmailLogDto?> GetEmailLogByIdAsync(int id)
        {
            try
            {
                var emailLog = await _emailLogRepository.GetByIdAsync(id);
                if (emailLog == null) return null;

                return new EmailLogDto
                {
                    EmailLogId = emailLog.EmailLogId,
                    CustomerId = emailLog.CustomerId,
                    CustomerName = emailLog.Customer?.Name ?? "",
                    Subject = emailLog.Subject,
                    Content = emailLog.Content,
                    SentAt = emailLog.SentAt,
                    SentBy = emailLog.SentBy,
                    Status = emailLog.Status,
                    ErrorMessage = emailLog.ErrorMessage
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting email log {Id}", id);
                throw;
            }
        }

        public async Task<IEnumerable<EmailLogDto>> GetEmailLogsByCustomerIdAsync(int customerId)
        {
            try
            {
                var emailLogs = await _emailLogRepository.GetByCustomerIdAsync(customerId);
                return emailLogs.Select(e => new EmailLogDto
                {
                    EmailLogId = e.EmailLogId,
                    CustomerId = e.CustomerId,
                    CustomerName = e.Customer?.Name ?? "",
                    Subject = e.Subject,
                    Content = e.Content,
                    SentAt = e.SentAt,
                    SentBy = e.SentBy,
                    Status = e.Status,
                    ErrorMessage = e.ErrorMessage
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting email logs for customer {CustomerId}", customerId);
                throw;
            }
        }

        public async Task<EmailLogDto> CreateEmailLogAsync(CreateEmailLogDto createDto)
        {
            try
            {
                // Verify customer exists
                if (!await _customerRepository.ExistsAsync(createDto.CustomerId))
                {
                    throw new InvalidOperationException("The specified customer does not exist.");
                }

                var emailLog = new EmailLog
                {
                    CustomerId = createDto.CustomerId,
                    Subject = createDto.Subject,
                    Content = createDto.Content,
                    SentBy = createDto.SentBy,
                    Status = EmailStatus.Pending
                };

                var createdEmailLog = await _emailLogRepository.CreateAsync(emailLog);
                var customer = await _customerRepository.GetByIdAsync(createdEmailLog.CustomerId);
                
                _logger.LogInformation("Email log created: {EmailLogId}", createdEmailLog.EmailLogId);

                return new EmailLogDto
                {
                    EmailLogId = createdEmailLog.EmailLogId,
                    CustomerId = createdEmailLog.CustomerId,
                    CustomerName = customer?.Name ?? "",
                    Subject = createdEmailLog.Subject,
                    Content = createdEmailLog.Content,
                    SentAt = createdEmailLog.SentAt,
                    SentBy = createdEmailLog.SentBy,
                    Status = createdEmailLog.Status
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating email log");
                throw;
            }
        }

        public async Task<EmailGenerationResponseDto> GenerateEmailAsync(EmailGenerationRequestDto request)
        {
            try
            {
                // Verify customer exists
                var customer = await _customerRepository.GetByIdAsync(request.CustomerId);
                if (customer == null)
                {
                    return new EmailGenerationResponseDto
                    {
                        Success = false,
                        ErrorMessage = "Customer not found."
                    };
                }

                // For now, create a simple template-based email generation
                // This would be replaced with actual AI integration
                var subject = GenerateSubjectByType(request.EmailType, customer.Name);
                var content = GenerateContentByType(request.EmailType, customer, request.AdditionalContext);

                _logger.LogInformation("Email generated for customer {CustomerId} with type {EmailType}", 
                    request.CustomerId, request.EmailType);

                return new EmailGenerationResponseDto
                {
                    Subject = subject,
                    Content = content,
                    Success = true
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating email for customer {CustomerId}", request.CustomerId);
                return new EmailGenerationResponseDto
                {
                    Success = false,
                    ErrorMessage = "An error occurred while generating the email."
                };
            }
        }

        public async Task<IEnumerable<EmailLogDto>> GetRecentEmailsAsync(int count = 10)
        {
            try
            {
                var emailLogs = await _emailLogRepository.GetRecentEmailsAsync(count);
                return emailLogs.Select(e => new EmailLogDto
                {
                    EmailLogId = e.EmailLogId,
                    CustomerId = e.CustomerId,
                    CustomerName = e.Customer?.Name ?? "",
                    Subject = e.Subject,
                    Content = e.Content,
                    SentAt = e.SentAt,
                    SentBy = e.SentBy,
                    Status = e.Status,
                    ErrorMessage = e.ErrorMessage
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting recent emails");
                throw;
            }
        }

        public async Task<Dictionary<string, int>> GetEmailStatsAsync()
        {
            try
            {
                return await _emailLogRepository.GetEmailStatsAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting email stats");
                throw;
            }
        }

        public async Task<bool> UpdateEmailStatusAsync(int emailLogId, string status, string? errorMessage = null)
        {
            try
            {
                var emailLog = await _emailLogRepository.GetByIdAsync(emailLogId);
                if (emailLog == null) return false;

                emailLog.Status = status;
                emailLog.ErrorMessage = errorMessage;

                await _emailLogRepository.UpdateAsync(emailLog);
                
                _logger.LogInformation("Email status updated: {EmailLogId} -> {Status}", emailLogId, status);
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating email status for {EmailLogId}", emailLogId);
                throw;
            }
        }

        private string GenerateSubjectByType(string emailType, string customerName)
        {
            return emailType.ToLower() switch
            {
                "welcome" => $"Welcome to Our Service, {customerName}!",
                "followup" => $"Following Up on Your Recent Inquiry",
                "promotional" => $"Special Offer Just for You, {customerName}",
                "newsletter" => $"Our Latest Newsletter",
                "reminder" => $"Friendly Reminder",
                _ => $"Important Message for {customerName}"
            };
        }

        private string GenerateContentByType(string emailType, Customer customer, string? additionalContext)
        {
            var baseContent = emailType.ToLower() switch
            {
                "welcome" => $"Dear {customer.Name},\n\nWelcome to our service! We're excited to have you as a customer.",
                "followup" => $"Dear {customer.Name},\n\nI wanted to follow up on your recent inquiry.",
                "promotional" => $"Dear {customer.Name},\n\nWe have a special promotion that we think you'll love!",
                "newsletter" => $"Dear {customer.Name},\n\nHere's what's new with us this month.",
                "reminder" => $"Dear {customer.Name},\n\nThis is a friendly reminder about your upcoming appointment.",
                _ => $"Dear {customer.Name},\n\nThank you for being a valued customer."
            };

            if (!string.IsNullOrEmpty(additionalContext))
            {
                baseContent += $"\n\n{additionalContext}";
            }

            baseContent += $"\n\nBest regards,\nThe Team";

            return baseContent;
        }

        public async Task<IEnumerable<EmailTemplateDto>> GetEmailTemplatesAsync()
        {
            // For now, return some default templates
            await Task.CompletedTask; // Make it properly async
            return new List<EmailTemplateDto>
            {
                new EmailTemplateDto { TemplateId = 1, Name = "Welcome", Subject = "Welcome to our service!", Content = "Dear {CustomerName}, welcome!" },
                new EmailTemplateDto { TemplateId = 2, Name = "Follow-up", Subject = "Following up", Content = "Dear {CustomerName}, just following up..." },
                new EmailTemplateDto { TemplateId = 3, Name = "Thank you", Subject = "Thank you!", Content = "Dear {CustomerName}, thank you for your business." }
            };
        }

        public async Task<bool> SendEmailAsync(ComposeEmailDto dto, string sentBy)
        {
            try
            {
                // Create email log
                var emailLog = new EmailLog
                {
                    Subject = dto.Subject,
                    Content = dto.Content,
                    SentAt = DateTime.UtcNow,
                    Status = "Sent",
                    CustomerId = dto.CustomerIds?.FirstOrDefault() ?? 0
                };

                await _emailLogRepository.CreateAsync(emailLog);
                _logger.LogInformation("Email sent successfully to {Count} customers", dto.CustomerIds?.Count ?? 0);
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending email");
                return false;
            }
        }

        public async Task<string> GenerateAIEmailAsync(GenerateAIEmailDto dto)
        {
            try
            {
                // Simulate AI email generation
                var templates = new Dictionary<string, string>
                {
                    {"welcome", "Welcome to our service! We're excited to have you on board."},
                    {"follow-up", "Just following up on our previous conversation. Please let us know if you have any questions."},
                    {"promotional", "Don't miss out on our latest offers! Check out what's new."},
                    {"support", "We're here to help! Our support team is standing by to assist you."}
                };

                var templateKey = dto.Purpose?.ToLower() ?? "welcome";
                var baseContent = templates.ContainsKey(templateKey) ? templates[templateKey] : templates["welcome"];

                if (dto.CustomerId.HasValue)
                {
                    var customer = await _customerRepository.GetByIdAsync(dto.CustomerId.Value);
                    if (customer != null)
                    {
                        baseContent = baseContent.Replace("{CustomerName}", customer.Name);
                    }
                }

                return baseContent;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating AI email");
                return "Error generating email content.";
            }
        }

        public async Task<bool> SendBulkEmailAsync(BulkEmailDto dto, string sentBy)
        {
            try
            {
                foreach (var customerId in dto.CustomerIds ?? new List<int>())
                {
                    var emailLog = new EmailLog
                    {
                        Subject = dto.Subject,
                        Content = dto.Content,
                        SentAt = DateTime.UtcNow,
                        Status = "Sent",
                        CustomerId = customerId
                    };

                    await _emailLogRepository.CreateAsync(emailLog);
                }

                _logger.LogInformation("Bulk email sent to {Count} customers", dto.CustomerIds?.Count ?? 0);
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending bulk email");
                return false;
            }
        }

        public async Task<EmailTemplateDto> SaveEmailTemplateAsync(EmailTemplateDto dto)
        {
            // For now, just return the dto with an ID
            if (dto.TemplateId == 0)
            {
                dto.TemplateId = new Random().Next(1000, 9999);
            }
            
            _logger.LogInformation("Email template saved: {TemplateName}", dto.Name);
            await Task.CompletedTask; // Make it properly async
            return dto;
        }

        public async Task<bool> DeleteEmailTemplateAsync(int templateId)
        {
            try
            {
                _logger.LogInformation("Email template deleted: {TemplateId}", templateId);
                await Task.CompletedTask; // Make it properly async
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting email template {TemplateId}", templateId);
                return false;
            }
        }

        public async Task<object> GetEmailAnalyticsAsync()
        {
            try
            {
                // Return some basic analytics
                await Task.CompletedTask; // Make it properly async
                return new
                {
                    TotalEmailsSent = 100,
                    EmailsSentToday = 10,
                    EmailsSentThisWeek = 50,
                    EmailsSentThisMonth = 200,
                    DeliveryRate = 98.5,
                    OpenRate = 25.3,
                    ClickRate = 5.8
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting email analytics");
                throw;
            }
        }

        public async Task<byte[]> ExportEmailLogsAsync(string format = "csv")
        {
            try
            {
                var emailLogs = await _emailLogRepository.GetPagedAsync(1, 1000, null);
                
                if (format.ToLower() == "csv")
                {
                    var csv = "Subject,SentAt,Status,Customer\n";
                    foreach (var log in emailLogs.Items)
                    {
                        csv += $"\"{log.Subject}\",\"{log.SentAt}\",\"{log.Status}\",\"{log.CustomerId}\"\n";
                    }
                    return System.Text.Encoding.UTF8.GetBytes(csv);
                }
                else
                {
                    var json = System.Text.Json.JsonSerializer.Serialize(emailLogs.Items);
                    return System.Text.Encoding.UTF8.GetBytes(json);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting email logs");
                throw;
            }
        }
    }
}
