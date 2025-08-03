using System.ComponentModel.DataAnnotations;

namespace MyCRM.Models.DTOs
{
    public class EmailGenerationDto
    {
        [Required]
        public int CustomerId { get; set; }

        [Required]
        [StringLength(50)]
        public string EmailType { get; set; } = string.Empty;

        [Required]
        [StringLength(1000)]
        public string TemplateText { get; set; } = string.Empty;

        [StringLength(255)]
        public string? Subject { get; set; }
    }

    public class BulkEmailGenerationDto
    {
        [Required]
        [MinLength(1)]
        public List<int> CustomerIds { get; set; } = new List<int>();

        [Required]
        [StringLength(50)]
        public string EmailType { get; set; } = string.Empty;

        [Required]
        [StringLength(1000)]
        public string TemplateText { get; set; } = string.Empty;

        [StringLength(255)]
        public string? Subject { get; set; }
    }

    public class EmailPreviewDto
    {
        public int CustomerId { get; set; }
        public string CustomerName { get; set; } = string.Empty;
        public string CustomerEmail { get; set; } = string.Empty;
        public string CustomerCompany { get; set; } = string.Empty;
        public string EmailType { get; set; } = string.Empty;
        public string Subject { get; set; } = string.Empty;
        public string GeneratedContent { get; set; } = string.Empty;
        public string TemplateText { get; set; } = string.Empty;
        public bool HipaaCompliant { get; set; }
        public string? HipaaAnalysis { get; set; }
        public bool ResponsibleAiCompliant { get; set; }
        public string? ResponsibleAiAnalysis { get; set; }
        public bool CanSend { get; set; }
    }

    public class BulkEmailPreviewDto
    {
        public List<EmailPreviewDto> EmailPreviews { get; set; } = new List<EmailPreviewDto>();
        public int TotalEmails { get; set; }
        public int CompliantEmails { get; set; }
        public int NonCompliantEmails { get; set; }
        public string EmailType { get; set; } = string.Empty;
        public string TemplateText { get; set; } = string.Empty;
    }

    public class SendEmailDto
    {
        [Required]
        public int CustomerId { get; set; }

        [Required]
        [StringLength(255)]
        public string Subject { get; set; } = string.Empty;

        [Required]
        [StringLength(2000)]
        public string Content { get; set; } = string.Empty;

        [Required]
        [StringLength(50)]
        public string EmailType { get; set; } = string.Empty;

        [StringLength(1000)]
        public string? TemplateText { get; set; }
    }

    public class BulkSendEmailDto
    {
        [Required]
        [MinLength(1)]
        public List<SendEmailDto> Emails { get; set; } = new List<SendEmailDto>();
    }

    public class EmailLogDto
    {
        public int EmailLogId { get; set; }
        public int CustomerId { get; set; }
        public string? CustomerName { get; set; }
        public string Subject { get; set; } = string.Empty;
        public string Content { get; set; } = string.Empty;
        public DateTime SentAt { get; set; }
        public string? SentBy { get; set; }
        public string Status { get; set; } = string.Empty;
        public string? ErrorMessage { get; set; }
    }

    public class SendEmailResultDto
    {
        public bool Success { get; set; }
        public string? Message { get; set; }
        public int? EmailLogId { get; set; }
    }

    public class BulkSendResultDto
    {
        public int TotalEmails { get; set; }
        public int SuccessfulSends { get; set; }
        public int FailedSends { get; set; }
        public List<SendEmailResultDto> Results { get; set; } = new List<SendEmailResultDto>();
    }

    public class CreateEmailLogDto
    {
        [Required]
        public int CustomerId { get; set; }

        [Required]
        [StringLength(255)]
        public string Subject { get; set; } = string.Empty;

        [Required]
        public string Content { get; set; } = string.Empty;

        [Required]
        [StringLength(20)]
        public string Status { get; set; } = string.Empty;

        public string? ErrorMessage { get; set; }

        public string? SentBy { get; set; }
    }

    public class EmailGenerationRequestDto
    {
        [Required]
        public int CustomerId { get; set; }

        [Required]
        [StringLength(50)]
        public string EmailType { get; set; } = string.Empty;

        [StringLength(1000)]
        public string? AdditionalContext { get; set; }
    }

    public class EmailGenerationResponseDto
    {
        public bool Success { get; set; }
        public string? Subject { get; set; }
        public string? Content { get; set; }
        public string? ErrorMessage { get; set; }
    }
}
