using System.Collections.Generic;
using System.Threading.Tasks;
using CRMDbOAI.Models;

namespace CRMDbOAI.Repositories
{
    public interface IRoleRepository
    {
        Task<IEnumerable<role>> GetAllAsync();
        Task<role?> GetByIdAsync(int id);
        Task AddAsync(role entity);
        Task UpdateAsync(role entity);
        Task DeleteAsync(int id);
    }
}
