using Microsoft.EntityFrameworkCore;
using MyCRM.Data;
using MyCRM.Models;
using MyCRM.Models.DTOs;

namespace MyCRM.Repositories
{
    public class EmailLogRepository : IEmailLogRepository
    {
        private readonly CrmDbContext _context;

        public EmailLogRepository(CrmDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<EmailLog>> GetAllAsync()
        {
            return await _context.EmailLogs
                .Include(e => e.Customer)
                .OrderByDescending(e => e.SentAt)
                .ToListAsync();
        }

        public async Task<EmailLog?> GetByIdAsync(int id)
        {
            return await _context.EmailLogs
                .Include(e => e.Customer)
                .FirstOrDefaultAsync(e => e.EmailLogId == id);
        }

        public async Task<IEnumerable<EmailLog>> GetByCustomerIdAsync(int customerId)
        {
            return await _context.EmailLogs
                .Where(e => e.CustomerId == customerId)
                .OrderByDescending(e => e.SentAt)
                .ToListAsync();
        }

        public async Task<PagedResult<EmailLog>> GetPagedAsync(int page, int pageSize, string? searchTerm = null)
        {
            var query = _context.EmailLogs
                .Include(e => e.Customer)
                .AsQueryable();

            if (!string.IsNullOrEmpty(searchTerm))
            {
                query = query.Where(e => e.Subject.Contains(searchTerm) ||
                                   e.Content.Contains(searchTerm) ||
                                   e.Customer!.Name.Contains(searchTerm));
            }

            var totalCount = await query.CountAsync();
            var items = await query
                .OrderByDescending(e => e.SentAt)
                .Skip((page - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            return new PagedResult<EmailLog>
            {
                Items = items,
                TotalCount = totalCount,
                PageNumber = page,
                PageSize = pageSize
            };
        }

        public async Task<EmailLog> CreateAsync(EmailLog emailLog)
        {
            emailLog.SentAt = DateTime.UtcNow;
            _context.EmailLogs.Add(emailLog);
            await _context.SaveChangesAsync();
            return emailLog;
        }

        public async Task<EmailLog> UpdateAsync(EmailLog emailLog)
        {
            _context.EmailLogs.Update(emailLog);
            await _context.SaveChangesAsync();
            return emailLog;
        }

        public async Task<bool> DeleteAsync(int id)
        {
            var emailLog = await GetByIdAsync(id);
            if (emailLog == null) return false;

            _context.EmailLogs.Remove(emailLog);
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<bool> ExistsAsync(int id)
        {
            return await _context.EmailLogs.AnyAsync(e => e.EmailLogId == id);
        }

        public async Task<int> GetTotalCountAsync()
        {
            return await _context.EmailLogs.CountAsync();
        }

        public async Task<IEnumerable<EmailLog>> GetRecentEmailsAsync(int count = 10)
        {
            return await _context.EmailLogs
                .Include(e => e.Customer)
                .OrderByDescending(e => e.SentAt)
                .Take(count)
                .ToListAsync();
        }

        public async Task<IEnumerable<EmailLog>> GetEmailsByStatusAsync(string status)
        {
            return await _context.EmailLogs
                .Include(e => e.Customer)
                .Where(e => e.Status == status)
                .OrderByDescending(e => e.SentAt)
                .ToListAsync();
        }

        public async Task<Dictionary<string, int>> GetEmailStatsAsync()
        {
            return await _context.EmailLogs
                .GroupBy(e => e.Status)
                .ToDictionaryAsync(g => g.Key, g => g.Count());
        }
    }
}
