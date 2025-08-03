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
    public class RoleServiceTests
    {
        private CRMDbContext _context;
        private IRoleRepository _repository;
        private IRoleService _service;

        [SetUp]
        public void Setup()
        {
            var options = new DbContextOptionsBuilder<CRMDbContext>()
                .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
                .Options;
            _context = new CRMDbContext(options);
            _repository = new RoleRepository(_context);
            _service = new RoleService(_repository);
        }

        [Test]
        public async Task AddAsync_ShouldAddRole()
        {
            var role = new role
            {
                role_name = "Admin",
                description = "Administrator role"
            };
            await _service.AddAsync(role);
            var all = await _service.GetAllAsync();
            Assert.That(((List<role>)all).Count, Is.EqualTo(1));
        }

        [Test]
        public async Task GetByIdAsync_ShouldReturnRole()
        {
            var role = new role
            {
                role_name = "User",
                description = "User role"
            };
            await _service.AddAsync(role);
            var all = await _service.GetAllAsync();
            var first = ((List<role>)all)[0];
            var found = await _service.GetByIdAsync(first.role_id);
            Assert.That(found, Is.Not.Null);
            if (found != null)
                Assert.That(found.role_name, Is.EqualTo("User"));
        }

        [Test]
        public async Task UpdateAsync_ShouldUpdateRole()
        {
            var role = new role
            {
                role_name = "Manager",
                description = "Manager role"
            };
            await _service.AddAsync(role);
            var all = await _service.GetAllAsync();
            var first = ((List<role>)all)[0];
            first.description = "Updated description";
            await _service.UpdateAsync(first);
            var updated = await _service.GetByIdAsync(first.role_id);
            Assert.That(updated, Is.Not.Null);
            if (updated != null)
                Assert.That(updated.description, Is.EqualTo("Updated description"));
        }

        [Test]
        public async Task DeleteAsync_ShouldDeleteRole()
        {
            var role = new role
            {
                role_name = "Temp",
                description = "Temporary role"
            };
            await _service.AddAsync(role);
            var all = await _service.GetAllAsync();
            var first = ((List<role>)all)[0];
            await _service.DeleteAsync(first.role_id);
            var active = await _service.GetAllAsync();
            Assert.That(((List<role>)active).Count, Is.EqualTo(0));
        }
    }
}
