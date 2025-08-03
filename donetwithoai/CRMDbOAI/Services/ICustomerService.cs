using System.Collections.Generic;
using System.Threading.Tasks;
using CRMDbOAI.Models;

namespace CRMDbOAI.Services
{
    public interface ICustomerService
    {
        Task<IEnumerable<customer>> GetAllAsync();
        Task<customer?> GetByIdAsync(int id);
        Task AddAsync(customer entity);
        Task UpdateAsync(customer entity);
        Task DeleteAsync(int id);
    }
}
