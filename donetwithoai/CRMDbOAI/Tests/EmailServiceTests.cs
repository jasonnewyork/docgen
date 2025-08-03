using NUnit.Framework;
using static NUnit.Framework.Assert;
using CRMDbOAI.Services;
using CRMDbOAI.Models;
using OpenAI;
// Remove invalid using; completions are under OpenAI namespace
using System.Collections.Generic;
using System.Threading.Tasks;

namespace CRMDbOAI.Tests
{
    [TestFixture]
    public class EmailServiceTests
    {
        [Test]
        public async Task OpenAI_SimpleCompletion_ReturnsResponse()
        {
            var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY");
            Assert.That(apiKey, Is.Not.Null.And.Not.Empty, "OPENAI_API_KEY environment variable must be set.");

            // Use OpenAI.Chat.ChatClient for chat completions
            var client = new OpenAI.Chat.ChatClient(model: "gpt-3.5-turbo", apiKey: apiKey);
            var prompt = "Say hello world.";
            var completion = await client.CompleteChatAsync(prompt);

            // Debug output for OAI API call
            TestContext.WriteLine($"[OAI DEBUG] Prompt: {prompt}");
            if (completion?.Value?.Content?.Count > 0)
            {
                TestContext.WriteLine($"[OAI DEBUG] Output: {completion.Value.Content[0].Text}");
            }

            Assert.That(completion, Is.Not.Null);
            Assert.That(completion.Value, Is.Not.Null);
            Assert.That(completion.Value.Content.Count, Is.GreaterThan(0));
            Assert.That(completion.Value.Content[0].Text.ToLower(), Does.Contain("hello"));
        }

        private EmailService _service;

        [SetUp]
        public void Setup()
        {
            _service = new EmailService();
        }

        [Test]
        public async Task GenerateEmailsAsync_PersonalizesTemplateForEachCustomer()
        {
            var customers = new List<customer>
            {
                new customer { customer_id = 1, contact_first_name = "Alice", contact_last_name = "Smith", company_name = "Acme", contact_email = "alice@acme.com" },
                new customer { customer_id = 2, contact_first_name = "Bob", contact_last_name = "Brown", company_name = "BetaCorp", contact_email = "bob@betacorp.com" }
            };
            var template = "Hello {ContactName} from {CompanyName}, this is a test.";

            var emails = await _service.GenerateEmailsAsync(customers, template);

            Assert.That(emails.Count, Is.EqualTo(2));
            Assert.That(emails[0].Body, Does.Contain("Alice Smith"));
            Assert.That(emails[0].Body, Does.Contain("Acme"));
            Assert.That(emails[1].Body, Does.Contain("Bob Brown"));
            Assert.That(emails[1].Body, Does.Contain("BetaCorp"));
        }

        [Test]
        public async Task GenerateEmailsAsync_SetsComplianceSummaryAndIsCompliant()
        {
            var customers = new List<customer>
            {
                new customer { customer_id = 1, contact_first_name = "Alice", contact_last_name = "Smith", company_name = "Acme", contact_email = "alice@acme.com" }
            };
            var template = "Test email.";

            var emails = await _service.GenerateEmailsAsync(customers, template);

            Assert.That(emails[0].IsCompliant, Is.True);
            Assert.That(emails[0].ComplianceSummary.ToLower(), Does.Contain("compliant"));
        }

        [Test]
        public async Task SendEmailsAsync_CompletesWithoutError()
        {
            var emails = new List<GeneratedEmail>
            {
                new GeneratedEmail { CustomerId = 1, ToEmail = "alice@acme.com", Subject = "Test", Body = "Body", Preview = "Body", IsCompliant = true, ComplianceSummary = "Compliant" }
            };
            Assert.DoesNotThrowAsync(async () => await _service.SendEmailsAsync(emails));
        }
    }
}
