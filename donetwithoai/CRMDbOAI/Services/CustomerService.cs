using System.Collections.Generic;
using System.Threading.Tasks;
using CRMDbOAI.Models;
using CRMDbOAI.Repositories;

namespace CRMDbOAI.Services
{
    public class CustomerService : ICustomerService
    {
        private readonly ICustomerRepository _repository;

        public CustomerService(ICustomerRepository repository)
        {
            _repository = repository;
        }

        public async Task<IEnumerable<customer>> GetAllAsync()
        {
            return await _repository.GetAllAsync();
        }

        public async Task<customer?> GetByIdAsync(int id)
        {
            return await _repository.GetByIdAsync(id);
        }

        public async Task AddAsync(customer entity)
        {
            await _repository.AddAsync(entity);
        }

        public async Task UpdateAsync(customer entity)
        {
            await _repository.UpdateAsync(entity);
        }

        public async Task DeleteAsync(int id)
        {
            await _repository.DeleteAsync(id);
        }
    }
}
