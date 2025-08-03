using System.ComponentModel.DataAnnotations;

namespace MyCRM.Models
{
    public class UserRole
    {
        [Key]
        public int RoleId { get; set; }

        [Required]
        [StringLength(50)]
        public string RoleName { get; set; } = string.Empty;

        [StringLength(255)]
        public string? RoleDescription { get; set; }

        public DateTime CreatedDate { get; set; } = DateTime.UtcNow;

        // Navigation properties
        public virtual ICollection<User> Users { get; set; } = new List<User>();
    }

    public static class UserRoles
    {
        public const string Administrator = "Administrator";
        public const string User = "User";
        public const string PowerUser = "PowerUser";
        public const string CustomerManager = "CustomerManager";
    }
}
