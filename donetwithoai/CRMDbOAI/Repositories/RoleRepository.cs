using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using CRMDbOAI.Models;

namespace CRMDbOAI.Repositories
{
    public class RoleRepository : IRoleRepository
    {
        private readonly CRMDbContext _context;
        public RoleRepository(CRMDbContext context) => _context = context;
        public async Task<IEnumerable<role>> GetAllAsync() => await _context.roles.ToListAsync();
        public async Task<role?> GetByIdAsync(int id) => await _context.roles.FindAsync(id);
        public async Task AddAsync(role entity)
        {
            _context.roles.Add(entity);
            await _context.SaveChangesAsync();
        }
        public async Task UpdateAsync(role entity)
        {
            _context.roles.Update(entity);
            await _context.SaveChangesAsync();
        }
        public async Task DeleteAsync(int id)
        {
            var entity = await _context.roles.FindAsync(id);
            if (entity != null)
            {
                _context.roles.Remove(entity);
                await _context.SaveChangesAsync();
            }
        }
    }
}
