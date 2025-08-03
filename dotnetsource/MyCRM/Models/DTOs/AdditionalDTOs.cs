using System.ComponentModel.DataAnnotations;

namespace MyCRM.Models.DTOs
{
    // Email-related DTOs
    public class ComposeEmailDto
    {
        [Required]
        [StringLength(500, ErrorMessage = "Subject cannot be longer than 500 characters.")]
        public string Subject { get; set; } = string.Empty;

        [Required]
        [StringLength(10000, ErrorMessage = "Content cannot be longer than 10,000 characters.")]
        public string Content { get; set; } = string.Empty;

        public List<string>? Recipients { get; set; }
        public List<int>? CustomerIds { get; set; }
        public int? TemplateId { get; set; }
    }

    public class GenerateAIEmailDto
    {
        [Required]
        [StringLength(500, ErrorMessage = "Purpose cannot be longer than 500 characters.")]
        public string Purpose { get; set; } = string.Empty;

        [StringLength(100, ErrorMessage = "Tone cannot be longer than 100 characters.")]
        public string? Tone { get; set; }

        [StringLength(1000, ErrorMessage = "Additional context cannot be longer than 1,000 characters.")]
        public string? AdditionalContext { get; set; }

        public int? CustomerId { get; set; }
    }

    public class BulkEmailDto
    {
        [Required]
        [StringLength(500, ErrorMessage = "Subject cannot be longer than 500 characters.")]
        public string Subject { get; set; } = string.Empty;

        [Required]
        [StringLength(10000, ErrorMessage = "Content cannot be longer than 10,000 characters.")]
        public string Content { get; set; } = string.Empty;

        [Required]
        public string RecipientType { get; set; } = "all"; // all, active, company, custom

        public string? CompanyFilter { get; set; }
        public List<int>? CustomerIds { get; set; }
        public int? TemplateId { get; set; }
    }

    public class EmailTemplateDto
    {
        public int TemplateId { get; set; }

        [Required]
        [StringLength(100)]
        public string Name { get; set; } = string.Empty;

        [Required]
        [StringLength(500)]
        public string Subject { get; set; } = string.Empty;

        [Required]
        [StringLength(10000)]
        public string Content { get; set; } = string.Empty;

        [StringLength(500)]
        public string? Description { get; set; }

        public bool IsActive { get; set; } = true;

        public DateTime CreatedAt { get; set; }
        public string? CreatedBy { get; set; }

        public DateTime? UpdatedAt { get; set; }
        public string? UpdatedBy { get; set; }
    }

    public class EmailAnalyticsDto
    {
        public int TotalEmailsSent { get; set; }
        public int TotalEmailsFailed { get; set; }
        public int TotalCustomersEmailed { get; set; }
        public int EmailsSentToday { get; set; }
        public int EmailsSentThisWeek { get; set; }
        public int EmailsSentThisMonth { get; set; }
        public double SuccessRate { get; set; }
    }
}
