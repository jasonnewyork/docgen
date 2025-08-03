using CRMDbOAI.Models;
using System.Collections.Generic;
using System.Threading.Tasks;
using System;
using System.Linq;

namespace CRMDbOAI.Services
{
    public class EmailService : IEmailService
    {
        public EmailService() { }

        public async Task<List<GeneratedEmail>> GenerateEmailsAsync(List<customer> customers, string templateText)
        {
            var emails = new List<GeneratedEmail>();
            var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY");
            var model = "gpt-3.5-turbo";
            var client = new OpenAI.Chat.ChatClient(model: model, apiKey: apiKey);

            foreach (var customer in customers)
            {
                var contactName = $"{customer.contact_first_name} {customer.contact_last_name}".Trim();
                var personalizedPrompt = templateText
                    .Replace("{ContactName}", contactName)
                    .Replace("{CompanyName}", customer.company_name ?? "");

                // GenAI: Generate personalized email body
                var prompt = $"Generate a personalized outreach email for {contactName} at {customer.company_name}. Template: {personalizedPrompt}";
                System.Diagnostics.Debug.WriteLine($"[OAI DEBUG] INPUT: {prompt}");
                var completion = await client.CompleteChatAsync(prompt);
                string generatedBody = personalizedPrompt;
                if (completion?.Value?.Content?.Count > 0)
                {
                    generatedBody = completion.Value.Content[0].Text;
                    System.Diagnostics.Debug.WriteLine($"[OAI DEBUG] OUTPUT: {generatedBody}");
                }

                // GenAI: Compliance check (HIPAA & Responsible AI)
                var compliancePrompt = $"Review the following email for HIPAA and Microsoft Responsible AI compliance. Summarize any violations, or reply 'Compliant' if none. Email: {generatedBody}";
                System.Diagnostics.Debug.WriteLine($"[OAI DEBUG] INPUT: {compliancePrompt}");
                var complianceResult = await client.CompleteChatAsync(compliancePrompt);
                string complianceSummary = "Compliant";
                bool isCompliant = true;
                if (complianceResult?.Value?.Content?.Count > 0)
                {
                    complianceSummary = complianceResult.Value.Content[0].Text;
                    System.Diagnostics.Debug.WriteLine($"[OAI DEBUG] OUTPUT: {complianceSummary}");
                    isCompliant = complianceSummary.Trim().ToLower().Contains("compliant");
                }

                emails.Add(new GeneratedEmail
                {
                    CustomerId = customer.customer_id,
                    ToEmail = customer.contact_email ?? string.Empty,
                    Subject = $"Outreach to {contactName}",
                    Body = generatedBody,
                    Preview = generatedBody,
                    IsCompliant = isCompliant,
                    ComplianceSummary = complianceSummary
                });
            }
            return emails;
        }

        public async Task SendEmailsAsync(List<GeneratedEmail> emails)
        {
            using (var db = new CRMDbOAI.Models.CRMDbContext())
            {
                foreach (var email in emails)
                {
                    // Simulate sending email via SMTP
                    Console.WriteLine($"[SMTP SIM] TO: {email.ToEmail}\nSUBJECT: {email.Subject}\nBODY:\n{email.Body}");
                    // TODO: Integrate actual SMTP sending here

                    // Log email activity to database
                    var log = new CRMDbOAI.Models.email_log
                    {
                        customer_id = email.CustomerId,
                        user_id = 1, // TODO: Replace with actual user id from context/session
                        email_type = "outreach", // TODO: Use actual type if available
                        subject = email.Subject,
                        content = email.Body,
                        recipient_email = email.ToEmail,
                        sent_date = DateTime.UtcNow,
                        status = "sent",
                        error_message = null
                    };
                    db.email_logs.Add(log);
                }
                await db.SaveChangesAsync();
            }
        }
    }
}
