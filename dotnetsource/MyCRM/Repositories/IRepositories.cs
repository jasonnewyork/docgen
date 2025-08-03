using MyCRM.Models;
using MyCRM.Models.DTOs;

namespace MyCRM.Repositories
{
    public interface ICustomerRepository
    {
        Task<IEnumerable<Customer>> GetAllAsync();
        Task<Customer?> GetByIdAsync(int id);
        Task<Customer?> GetByEmailAsync(string email);
        Task<PagedResult<Customer>> GetPagedAsync(int page, int pageSize, string? searchTerm = null);
        Task<Customer> CreateAsync(Customer customer);
        Task<Customer> UpdateAsync(Customer customer);
        Task<bool> DeleteAsync(int id);
        Task<bool> ExistsAsync(int id);
        Task<bool> EmailExistsAsync(string email, int? excludeId = null);
        Task<int> GetTotalCountAsync();
        Task<IEnumerable<Customer>> GetActiveCustomersAsync();
    }

    public interface IUserRepository
    {
        Task<IEnumerable<User>> GetAllAsync();
        Task<User?> GetByIdAsync(int id);
        Task<User?> GetByUsernameAsync(string username);
        Task<User?> GetByEmailAsync(string email);
        Task<PagedResult<User>> GetPagedAsync(int page, int pageSize, string? searchTerm = null);
        Task<User> CreateAsync(User user);
        Task<User> UpdateAsync(User user);
        Task<bool> DeleteAsync(int id);
        Task<bool> ExistsAsync(int id);
        Task<bool> UsernameExistsAsync(string username, int? excludeId = null);
        Task<bool> EmailExistsAsync(string email, int? excludeId = null);
        Task<int> GetTotalCountAsync();
        Task<IEnumerable<User>> GetActiveUsersAsync();
        Task UpdateLastLoginAsync(int userId);
        Task IncrementFailedLoginAttemptsAsync(int userId);
        Task ResetFailedLoginAttemptsAsync(int userId);
        Task SetLockoutAsync(int userId, DateTime lockoutEnd);
    }

    public interface IEmailLogRepository
    {
        Task<IEnumerable<EmailLog>> GetAllAsync();
        Task<EmailLog?> GetByIdAsync(int id);
        Task<IEnumerable<EmailLog>> GetByCustomerIdAsync(int customerId);
        Task<PagedResult<EmailLog>> GetPagedAsync(int page, int pageSize, string? searchTerm = null);
        Task<EmailLog> CreateAsync(EmailLog emailLog);
        Task<EmailLog> UpdateAsync(EmailLog emailLog);
        Task<bool> DeleteAsync(int id);
        Task<bool> ExistsAsync(int id);
        Task<int> GetTotalCountAsync();
        Task<IEnumerable<EmailLog>> GetRecentEmailsAsync(int count = 10);
        Task<IEnumerable<EmailLog>> GetEmailsByStatusAsync(string status);
        Task<Dictionary<string, int>> GetEmailStatsAsync();
    }

    public interface IUserRoleRepository
    {
        Task<IEnumerable<UserRole>> GetAllAsync();
        Task<UserRole?> GetByIdAsync(int id);
        Task<UserRole?> GetByNameAsync(string name);
        Task<UserRole> CreateAsync(UserRole role);
        Task<UserRole> UpdateAsync(UserRole role);
        Task<bool> DeleteAsync(int id);
        Task<bool> ExistsAsync(int id);
        Task<bool> NameExistsAsync(string name, int? excludeId = null);
    }
}
