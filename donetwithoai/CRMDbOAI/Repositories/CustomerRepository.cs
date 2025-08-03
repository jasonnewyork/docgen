using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using CRMDbOAI.Models;

namespace CRMDbOAI.Repositories
{
    public class CustomerRepository : ICustomerRepository
    {
        private readonly CRMDbContext _context;

        public CustomerRepository(CRMDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<customer>> GetAllAsync()
        {
            return await _context.customers.Where(c => c.is_active == true).ToListAsync();
        }

        public async Task<customer?> GetByIdAsync(int id)
        {
            return await _context.customers.FindAsync(id);
        }

        public async Task AddAsync(customer entity)
        {
            _context.customers.Add(entity);
            await _context.SaveChangesAsync();
        }

        public async Task UpdateAsync(customer entity)
        {
            _context.customers.Update(entity);
            await _context.SaveChangesAsync();
        }

        public async Task DeleteAsync(int id)
        {
            var entity = await _context.customers.FindAsync(id);
            if (entity != null)
            {
                entity.is_active = false;
                await _context.SaveChangesAsync();
            }
        }
    }
}
