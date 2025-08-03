using System.ComponentModel.DataAnnotations;

namespace MyCRM.Models.DTOs
{
    public class CustomerDto
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string? Company { get; set; }
        public string? Title { get; set; }
        public string? Phone { get; set; }
        public string? LinkedInUrl { get; set; }
        public string? Notes { get; set; }
        public bool IsActive { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime UpdatedAt { get; set; }
        public string? CreatedBy { get; set; }
        public string? UpdatedBy { get; set; }
    }

    public class CreateCustomerDto
    {
        [Required]
        [StringLength(100)]
        public string Name { get; set; } = string.Empty;

        [Required]
        [EmailAddress]
        [StringLength(100)]
        public string Email { get; set; } = string.Empty;

        [StringLength(100)]
        public string? Company { get; set; }

        [StringLength(50)]
        public string? Title { get; set; }

        [StringLength(20)]
        public string? Phone { get; set; }

        [StringLength(255)]
        [Url]
        public string? LinkedInUrl { get; set; }

        public string? Notes { get; set; }

        public bool IsActive { get; set; } = true;
    }

    public class UpdateCustomerDto
    {
        [Required]
        [StringLength(100)]
        public string Name { get; set; } = string.Empty;

        [Required]
        [EmailAddress]
        [StringLength(100)]
        public string Email { get; set; } = string.Empty;

        [StringLength(100)]
        public string? Company { get; set; }

        [StringLength(50)]
        public string? Title { get; set; }

        [StringLength(20)]
        public string? Phone { get; set; }

        [StringLength(255)]
        [Url]
        public string? LinkedInUrl { get; set; }

        public string? Notes { get; set; }

        public bool IsActive { get; set; }
    }
}
