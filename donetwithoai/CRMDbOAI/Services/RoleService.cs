using System.Collections.Generic;
using System.Threading.Tasks;
using CRMDbOAI.Models;
using CRMDbOAI.Repositories;

namespace CRMDbOAI.Services
{
    public class RoleService : IRoleService
    {
        private readonly IRoleRepository _repo;
        public RoleService(IRoleRepository repo) => _repo = repo;
        public Task<IEnumerable<role>> GetAllAsync() => _repo.GetAllAsync();
        public Task<role?> GetByIdAsync(int id) => _repo.GetByIdAsync(id);
        public Task AddAsync(role entity) => _repo.AddAsync(entity);
        public Task UpdateAsync(role entity) => _repo.UpdateAsync(entity);
        public Task DeleteAsync(int id) => _repo.DeleteAsync(id);
    }
}
