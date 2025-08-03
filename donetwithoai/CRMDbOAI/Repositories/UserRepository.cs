using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using CRMDbOAI.Models;

namespace CRMDbOAI.Repositories
{
    public class UserRepository : IUserRepository
    {
        private readonly CRMDbContext _context;
        public UserRepository(CRMDbContext context) => _context = context;
        public async Task<IEnumerable<user>> GetAllAsync() => await _context.users.ToListAsync();
        public async Task<user?> GetByIdAsync(int id) => await _context.users.FindAsync(id);
        public async Task AddAsync(user entity)
        {
            _context.users.Add(entity);
            await _context.SaveChangesAsync();
        }
        public async Task UpdateAsync(user entity)
        {
            _context.users.Update(entity);
            await _context.SaveChangesAsync();
        }
        public async Task DeleteAsync(int id)
        {
            var entity = await _context.users.FindAsync(id);
            if (entity != null)
            {
                entity.is_active = false;
                await _context.SaveChangesAsync();
            }
        }
    }
}
