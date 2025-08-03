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
    public class UserServiceTests
    {
        private CRMDbContext _context;
        private IUserRepository _repository;
        private IUserService _service;

        [SetUp]
        public void Setup()
        {
            var options = new DbContextOptionsBuilder<CRMDbContext>()
                .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
                .Options;
            _context = new CRMDbContext(options);
            _repository = new UserRepository(_context);
            _service = new UserService(_repository);
        }

        [Test]
        public async Task AddAsync_ShouldAddUser()
        {
            var user = new user
            {
                username = "testuser",
                email = "testuser@example.com",
                first_name = "Test",
                last_name = "User",
                password_hash = "hashedpassword",
                is_active = true
            };
            await _service.AddAsync(user);
            var all = await _service.GetAllAsync();
            Assert.That(((List<user>)all).Count, Is.EqualTo(1));
        }

        [Test]
        public async Task GetByIdAsync_ShouldReturnUser()
        {
            var user = new user
            {
                username = "testuser2",
                email = "testuser2@example.com",
                first_name = "Jane",
                last_name = "Smith",
                password_hash = "hashedpassword",
                is_active = true
            };
            await _service.AddAsync(user);
            var all = await _service.GetAllAsync();
            var first = ((List<user>)all)[0];
            var found = await _service.GetByIdAsync(first.user_id);
            Assert.That(found, Is.Not.Null);
            if (found != null)
                Assert.That(found.username, Is.EqualTo("testuser2"));
        }

        [Test]
        public async Task UpdateAsync_ShouldUpdateUser()
        {
            var user = new user
            {
                username = "testuser3",
                email = "testuser3@example.com",
                first_name = "Alice",
                last_name = "Brown",
                password_hash = "hashedpassword",
                is_active = true
            };
            await _service.AddAsync(user);
            var all = await _service.GetAllAsync();
            var first = ((List<user>)all)[0];
            first.first_name = "Alicia";
            await _service.UpdateAsync(first);
            var updated = await _service.GetByIdAsync(first.user_id);
            Assert.That(updated, Is.Not.Null);
            if (updated != null)
                Assert.That(updated.first_name, Is.EqualTo("Alicia"));
        }

        [Test]
        public async Task DeleteAsync_ShouldSoftDeleteUser()
        {
            var user = new user
            {
                username = "testuser4",
                email = "testuser4@example.com",
                first_name = "Bob",
                last_name = "White",
                password_hash = "hashedpassword",
                is_active = true
            };
            await _service.AddAsync(user);
            var all = await _service.GetAllAsync();
            var first = ((List<user>)all)[0];
            await _service.DeleteAsync(first.user_id);
            var active = await _service.GetAllAsync();
            var activeUsers = ((List<user>)active).FindAll(u => u.is_active == true);
            Assert.That(activeUsers.Count, Is.EqualTo(0));
            var deleted = await _service.GetByIdAsync(first.user_id);
            Assert.That(deleted, Is.Not.Null);
            if (deleted != null)
                Assert.That(deleted.is_active ?? true, Is.False);
        }
    }
}
