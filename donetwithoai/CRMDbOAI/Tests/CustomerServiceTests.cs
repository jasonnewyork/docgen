using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using CRMDbOAI.Models;
using CRMDbOAI.Repositories;
using CRMDbOAI.Services;
using Microsoft.EntityFrameworkCore;
using NUnit.Framework;

namespace CRMDbOAI.Tests
{
    [TestFixture]
    public class CustomerServiceTests
    {
        private CRMDbContext _context;
        private ICustomerRepository _repository;
        private ICustomerService _service;

        [SetUp]
        public void Setup()
        {
            var options = new DbContextOptionsBuilder<CRMDbContext>()
                .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
                .Options;
        _context = new CRMDbContext(options);
        // Do not use DI registration from Program.cs; instantiate directly for test isolation
        _repository = new Repositories.CustomerRepository(_context);
        _service = new Services.CustomerService(_repository);
        }

        [Test]
        public async Task AddAsync_ShouldAddCustomer()
        {
            var customer = new customer
            {
                company_name = "TestCo",
                contact_first_name = "John",
                contact_last_name = "Doe",
                contact_email = "john.doe@testco.com",
                is_active = true
            };
            await _service.AddAsync(customer);
            var all = await _service.GetAllAsync();
            Assert.That(((List<customer>)all).Count, Is.EqualTo(1));
        }

        [Test]
        public async Task GetByIdAsync_ShouldReturnCustomer()
        {
            var customer = new customer
            {
                company_name = "TestCo",
                contact_first_name = "Jane",
                contact_last_name = "Smith",
                contact_email = "jane.smith@testco.com",
                is_active = true
            };
            await _service.AddAsync(customer);
            var all = await _service.GetAllAsync();
            var first = ((List<customer>)all)[0];
            var found = await _service.GetByIdAsync(first.customer_id);
            Assert.That(found, Is.Not.Null);
            if (found != null)
                Assert.That(found.contact_first_name, Is.EqualTo("Jane"));
        }

        [Test]
        public async Task UpdateAsync_ShouldUpdateCustomer()
        {
            var customer = new customer
            {
                company_name = "TestCo",
                contact_first_name = "Alice",
                contact_last_name = "Brown",
                contact_email = "alice.brown@testco.com",
                is_active = true
            };
            await _service.AddAsync(customer);
            var all = await _service.GetAllAsync();
            var first = ((List<customer>)all)[0];
            first.contact_first_name = "Alicia";
            await _service.UpdateAsync(first);
            var updated = await _service.GetByIdAsync(first.customer_id);
            Assert.That(updated, Is.Not.Null);
            if (updated != null)
                Assert.That(updated.contact_first_name, Is.EqualTo("Alicia"));
        }

        [Test]
        public async Task DeleteAsync_ShouldSoftDeleteCustomer()
        {
            var customer = new customer
            {
                company_name = "TestCo",
                contact_first_name = "Bob",
                contact_last_name = "White",
                contact_email = "bob.white@testco.com",
                is_active = true
            };
            await _service.AddAsync(customer);
            var all = await _service.GetAllAsync();
            var first = ((List<customer>)all)[0];
            await _service.DeleteAsync(first.customer_id);
            var active = await _service.GetAllAsync();
            Assert.That(((List<customer>)active).Count, Is.EqualTo(0));
            var deleted = await _service.GetByIdAsync(first.customer_id);
            Assert.That(deleted, Is.Not.Null);
            if (deleted != null)
                Assert.That(deleted.is_active ?? true, Is.False);
        }
    }
}
