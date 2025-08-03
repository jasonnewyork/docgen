using System.Collections.Generic;
using System.Threading.Tasks;
using CRMDbOAI.Models;
using CRMDbOAI.Repositories;

namespace CRMDbOAI.Services
{
    public class UserService : IUserService
    {
        private readonly IUserRepository _repo;
        public UserService(IUserRepository repo) => _repo = repo;
        public Task<IEnumerable<user>> GetAllAsync() => _repo.GetAllAsync();
        public Task<user?> GetByIdAsync(int id) => _repo.GetByIdAsync(id);
        public Task AddAsync(user entity) => _repo.AddAsync(entity);
        public Task UpdateAsync(user entity) => _repo.UpdateAsync(entity);
        public Task DeleteAsync(int id) => _repo.DeleteAsync(id);
    }
}
