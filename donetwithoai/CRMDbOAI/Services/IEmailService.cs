using CRMDbOAI.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace CRMDbOAI.Services
{
    public interface IEmailService
    {
        /// <summary>
        /// Generates personalized outreach emails for selected customers using a template and GenAI.
        /// </summary>
        /// <param name="customers">List of customers to email.</param>
        /// <param name="templateText">Template text (up to 1000 chars).</param>
        /// <returns>List of generated email objects (preview).</returns>
        Task<List<GeneratedEmail>> GenerateEmailsAsync(List<customer> customers, string templateText);

        /// <summary>
        /// Sends the generated emails and logs the activity.
        /// </summary>
        /// <param name="emails">List of emails to send.</param>
        /// <returns>Task for async operation.</returns>
        Task SendEmailsAsync(List<GeneratedEmail> emails);
    }

    public class GeneratedEmail
    {
        public int CustomerId { get; set; }
        public string ToEmail { get; set; }
        public string Subject { get; set; }
        public string Body { get; set; }
        public string Preview { get; set; }
        public bool IsCompliant { get; set; } // For Responsible AI/HIPAA
        public string ComplianceSummary { get; set; }
    }
}
