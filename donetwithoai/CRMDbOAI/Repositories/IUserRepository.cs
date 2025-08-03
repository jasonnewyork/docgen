using System.Collections.Generic;
using System.Threading.Tasks;
using CRMDbOAI.Models;

namespace CRMDbOAI.Repositories
{
    public interface IUserRepository
    {
        Task<IEnumerable<user>> GetAllAsync();
        Task<user?> GetByIdAsync(int id);
        Task AddAsync(user entity);
        Task UpdateAsync(user entity);
        Task DeleteAsync(int id);
    }
}
