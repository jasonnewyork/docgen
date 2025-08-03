using Microsoft.EntityFrameworkCore;
using MyCRM.Data;
using MyCRM.Models;

namespace MyCRM.Repositories
{
    public class UserRoleRepository : IUserRoleRepository
    {
        private readonly CrmDbContext _context;

        public UserRoleRepository(CrmDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<UserRole>> GetAllAsync()
        {
            return await _context.UserRoles
                .OrderBy(r => r.RoleName)
                .ToListAsync();
        }

        public async Task<UserRole?> GetByIdAsync(int id)
        {
            return await _context.UserRoles.FindAsync(id);
        }

        public async Task<UserRole?> GetByNameAsync(string name)
        {
            return await _context.UserRoles
                .FirstOrDefaultAsync(r => r.RoleName == name);
        }

        public async Task<UserRole> CreateAsync(UserRole role)
        {
            _context.UserRoles.Add(role);
            await _context.SaveChangesAsync();
            return role;
        }

        public async Task<UserRole> UpdateAsync(UserRole role)
        {
            _context.Entry(role).State = EntityState.Modified;
            await _context.SaveChangesAsync();
            return role;
        }

        public async Task<bool> DeleteAsync(int id)
        {
            var role = await _context.UserRoles.FindAsync(id);
            if (role == null) return false;

            _context.UserRoles.Remove(role);
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<bool> ExistsAsync(int id)
        {
            return await _context.UserRoles.AnyAsync(r => r.RoleId == id);
        }

        public async Task<bool> NameExistsAsync(string name, int? excludeId = null)
        {
            var query = _context.UserRoles.Where(r => r.RoleName == name);
            if (excludeId.HasValue)
            {
                query = query.Where(r => r.RoleId != excludeId.Value);
            }
            return await query.AnyAsync();
        }
    }
}
