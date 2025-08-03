using MyCRM.Data;
using MyCRM.Models;
using MyCRM.Models.DTOs;
using MyCRM.Repositories;
using Microsoft.Extensions.Logging;

namespace MyCRM.Services
{
    public class CustomerService
    {
        private readonly ICustomerRepository _customerRepository;
        private readonly IEmailLogRepository _emailLogRepository;
        private readonly ILogger<CustomerService> _logger;

        public CustomerService(ICustomerRepository customerRepository, IEmailLogRepository emailLogRepository, ILogger<CustomerService> logger)
        {
            _customerRepository = customerRepository;
            _emailLogRepository = emailLogRepository;
            _logger = logger;
        }

        public async Task<PagedResult<CustomerDto>> GetPagedCustomersAsync(int pageNumber, int pageSize, string? searchTerm)
        {
            try
            {
                var pagedResult = await _customerRepository.GetPagedAsync(pageNumber, pageSize, searchTerm);
                
                var customerDtos = pagedResult.Items.Select(c => new CustomerDto
                {
                    Id = c.Id,
                    Name = c.Name,
                    Email = c.Email,
                    Phone = c.Phone,
                    Company = c.Company,
                    Notes = c.Notes,
                    IsActive = c.IsActive,
                    CreatedAt = c.CreatedAt,
                    CreatedBy = c.CreatedBy,
                    UpdatedAt = c.UpdatedAt,
                    UpdatedBy = c.UpdatedBy
                }).ToList();

                return new PagedResult<CustomerDto>(
                    customerDtos,
                    pagedResult.TotalCount,
                    pagedResult.PageNumber,
                    pagedResult.PageSize
                );
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting paged customers");
                throw;
            }
        }

        public async Task<CustomerDto?> GetCustomerByIdAsync(int id)
        {
            try
            {
                var customer = await _customerRepository.GetByIdAsync(id);
                if (customer == null) return null;

                return new CustomerDto
                {
                    Id = customer.Id,
                    Name = customer.Name,
                    Email = customer.Email,
                    Phone = customer.Phone,
                    Company = customer.Company,
                    Notes = customer.Notes,
                    IsActive = customer.IsActive,
                    CreatedAt = customer.CreatedAt,
                    CreatedBy = customer.CreatedBy,
                    UpdatedAt = customer.UpdatedAt,
                    UpdatedBy = customer.UpdatedBy
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting customer by ID: {CustomerId}", id);
                throw;
            }
        }

        public async Task<CustomerDto> CreateCustomerAsync(CreateCustomerDto dto, string createdBy)
        {
            try
            {
                var customer = new Customer
                {
                    Name = dto.Name,
                    Email = dto.Email,
                    Phone = dto.Phone,
                    Company = dto.Company,
                    Notes = dto.Notes,
                    IsActive = true,
                    CreatedBy = createdBy,
                    CreatedAt = DateTime.UtcNow
                };

                var createdCustomer = await _customerRepository.CreateAsync(customer);
                
                _logger.LogInformation("Customer created: {CustomerId}", createdCustomer.Id);

                return new CustomerDto
                {
                    Id = createdCustomer.Id,
                    Name = createdCustomer.Name,
                    Email = createdCustomer.Email,
                    Phone = createdCustomer.Phone,
                    Company = createdCustomer.Company,
                    Notes = createdCustomer.Notes,
                    IsActive = createdCustomer.IsActive,
                    CreatedAt = createdCustomer.CreatedAt,
                    CreatedBy = createdCustomer.CreatedBy
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating customer");
                throw;
            }
        }

        public async Task<CustomerDto?> UpdateCustomerAsync(int id, UpdateCustomerDto dto, string updatedBy)
        {
            try
            {
                var customer = await _customerRepository.GetByIdAsync(id);
                if (customer == null) return null;

                customer.Name = dto.Name;
                customer.Email = dto.Email;
                customer.Phone = dto.Phone;
                customer.Company = dto.Company;
                customer.Notes = dto.Notes;
                customer.UpdatedBy = updatedBy;
                customer.UpdatedAt = DateTime.UtcNow;

                var updatedCustomer = await _customerRepository.UpdateAsync(customer);
                
                _logger.LogInformation("Customer updated: {CustomerId}", updatedCustomer.Id);

                return new CustomerDto
                {
                    Id = updatedCustomer.Id,
                    Name = updatedCustomer.Name,
                    Email = updatedCustomer.Email,
                    Phone = updatedCustomer.Phone,
                    Company = updatedCustomer.Company,
                    Notes = updatedCustomer.Notes,
                    IsActive = updatedCustomer.IsActive,
                    CreatedAt = updatedCustomer.CreatedAt,
                    CreatedBy = updatedCustomer.CreatedBy,
                    UpdatedAt = updatedCustomer.UpdatedAt,
                    UpdatedBy = updatedCustomer.UpdatedBy
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating customer: {CustomerId}", id);
                throw;
            }
        }

        public async Task<bool> DeleteCustomerAsync(int id)
        {
            try
            {
                var success = await _customerRepository.DeleteAsync(id);
                
                if (success)
                {
                    _logger.LogInformation("Customer deleted: {CustomerId}", id);
                }
                
                return success;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting customer: {CustomerId}", id);
                throw;
            }
        }

        public async Task<bool> DeactivateCustomerAsync(int id, string deactivatedBy)
        {
            try
            {
                var customer = await _customerRepository.GetByIdAsync(id);
                if (customer == null) return false;

                customer.IsActive = false;
                customer.UpdatedBy = deactivatedBy;
                customer.UpdatedAt = DateTime.UtcNow;

                await _customerRepository.UpdateAsync(customer);
                
                _logger.LogInformation("Customer deactivated: {CustomerId}", id);
                
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deactivating customer: {CustomerId}", id);
                throw;
            }
        }

        public async Task<IEnumerable<CustomerDto>> GetActiveCustomersAsync()
        {
            try
            {
                var customers = await _customerRepository.GetActiveCustomersAsync();
                return customers.Select(c => new CustomerDto
                {
                    Id = c.Id,
                    Name = c.Name,
                    Email = c.Email,
                    Phone = c.Phone,
                    Company = c.Company,
                    Notes = c.Notes,
                    IsActive = c.IsActive,
                    CreatedAt = c.CreatedAt,
                    CreatedBy = c.CreatedBy,
                    UpdatedAt = c.UpdatedAt,
                    UpdatedBy = c.UpdatedBy
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting active customers");
                throw;
            }
        }

        public async Task<bool> CustomerExistsAsync(int id)
        {
            try
            {
                var customer = await _customerRepository.GetByIdAsync(id);
                return customer != null;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error checking if customer exists: {CustomerId}", id);
                throw;
            }
        }

        public async Task<IEnumerable<EmailLogDto>> GetCustomerEmailHistoryAsync(int customerId)
        {
            try
            {
                var emailLogs = await _emailLogRepository.GetByCustomerIdAsync(customerId);
                return emailLogs.Select(e => new EmailLogDto
                {
                    EmailLogId = e.EmailLogId,
                    CustomerId = e.CustomerId,
                    Subject = e.Subject,
                    Content = e.Content,
                    SentAt = e.SentAt,
                    SentBy = e.SentBy,
                    Status = e.Status,
                    ErrorMessage = e.ErrorMessage
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting customer email history: {CustomerId}", customerId);
                throw;
            }
        }

        public async Task<IEnumerable<CustomerDto>> ImportCustomersAsync(IFormFile file, string importedBy)
        {
            try
            {
                // For now, return empty list
                await Task.CompletedTask;
                _logger.LogInformation("Customers imported by {ImportedBy}", importedBy);
                return new List<CustomerDto>();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error importing customers");
                throw;
            }
        }

        public async Task<byte[]> ExportCustomersAsync(string format = "csv")
        {
            try
            {
                var customers = await _customerRepository.GetPagedAsync(1, 1000, null);
                
                if (format.ToLower() == "csv")
                {
                    var csv = "Name,Email,Phone,Company,IsActive,CreatedAt\n";
                    foreach (var customer in customers.Items)
                    {
                        csv += $"\"{customer.Name}\",\"{customer.Email}\",\"{customer.Phone}\",\"{customer.Company}\",\"{customer.IsActive}\",\"{customer.CreatedAt}\"\n";
                    }
                    return System.Text.Encoding.UTF8.GetBytes(csv);
                }
                else
                {
                    var json = System.Text.Json.JsonSerializer.Serialize(customers.Items);
                    return System.Text.Encoding.UTF8.GetBytes(json);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting customers");
                throw;
            }
        }
    }
}
