using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

namespace CRMDbOAI.Models;

public partial class CRMDbContext : DbContext
{
    public CRMDbContext()
    {
    }

    public CRMDbContext(DbContextOptions<CRMDbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<customer> customers { get; set; }

    public virtual DbSet<email_log> email_logs { get; set; }

    public virtual DbSet<role> roles { get; set; }

    public virtual DbSet<user> users { get; set; }

protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
#warning To protect potentially sensitive information in your connection string, you should move it out of source code. You can avoid scaffolding the connection string by using the Name= syntax to read it from configuration - see https://go.microsoft.com/fwlink/?linkid=2131148. For more guidance on storing connection strings, see https://go.microsoft.com/fwlink/?LinkId=723263.
    {
        if (!optionsBuilder.IsConfigured)
        {
            optionsBuilder.UseSqlServer("Server=localhost;Database=CRMDb;User Id=sa;Password=" + Environment.GetEnvironmentVariable("SQL_PASSWORD") + ";TrustServerCertificate=True;");
        }
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<customer>(entity =>
        {
            entity.HasKey(e => e.customer_id).HasName("PK__customer__CD65CB851D174C71");

            entity.HasIndex(e => e.company_name, "IX_Customers_CompanyName");

            entity.HasIndex(e => e.contact_email, "IX_Customers_ContactEmail");

            entity.Property(e => e.address).HasMaxLength(255);
            entity.Property(e => e.city).HasMaxLength(100);
            entity.Property(e => e.company_name).HasMaxLength(255);
            entity.Property(e => e.contact_email).HasMaxLength(255);
            entity.Property(e => e.contact_first_name).HasMaxLength(100);
            entity.Property(e => e.contact_last_name).HasMaxLength(100);
            entity.Property(e => e.contact_phone).HasMaxLength(50);
            entity.Property(e => e.country).HasMaxLength(100);
            entity.Property(e => e.created_date).HasDefaultValueSql("(getdate())");
            entity.Property(e => e.industry).HasMaxLength(100);
            entity.Property(e => e.is_active).HasDefaultValue(true);
            entity.Property(e => e.last_modified_date).HasDefaultValueSql("(getdate())");
            entity.Property(e => e.postal_code).HasMaxLength(20);
            entity.Property(e => e.state).HasMaxLength(100);
        });

        modelBuilder.Entity<email_log>(entity =>
        {
            entity.HasKey(e => e.log_id).HasName("PK__email_lo__9E2397E05BC070BE");

            entity.HasIndex(e => e.customer_id, "IX_EmailLogs_CustomerID");

            entity.HasIndex(e => e.sent_date, "IX_EmailLogs_SentDate");

            entity.HasIndex(e => e.user_id, "IX_EmailLogs_UserID");

            entity.Property(e => e.content).HasColumnType("ntext");
            entity.Property(e => e.email_type).HasMaxLength(50);
            entity.Property(e => e.error_message).HasColumnType("ntext");
            entity.Property(e => e.recipient_email).HasMaxLength(255);
            entity.Property(e => e.sent_date).HasDefaultValueSql("(getdate())");
            entity.Property(e => e.status)
                .HasMaxLength(50)
                .HasDefaultValue("Pending");
            entity.Property(e => e.subject).HasMaxLength(255);

            entity.HasOne(d => d.customer).WithMany(p => p.email_logs)
                .HasForeignKey(d => d.customer_id)
                .HasConstraintName("FK_EmailLogs_Customers");

            entity.HasOne(d => d.user).WithMany(p => p.email_logs)
                .HasForeignKey(d => d.user_id)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("FK_EmailLogs_Users");
        });

        modelBuilder.Entity<role>(entity =>
        {
            entity.HasKey(e => e.role_id).HasName("PK__roles__760965CC712A4162");

            entity.HasIndex(e => e.role_name, "UQ__roles__783254B1782B6BA4").IsUnique();

            entity.Property(e => e.created_date).HasDefaultValueSql("(getdate())");
            entity.Property(e => e.description).HasMaxLength(255);
            entity.Property(e => e.role_name).HasMaxLength(50);
        });

        modelBuilder.Entity<user>(entity =>
        {
            entity.HasKey(e => e.user_id).HasName("PK__users__B9BE370FC9BFD2BD");

            entity.HasIndex(e => e.email, "IX_Users_Email");

            entity.HasIndex(e => e.username, "IX_Users_Username");

            entity.HasIndex(e => e.email, "UQ__users__AB6E61647178A788").IsUnique();

            entity.HasIndex(e => e.username, "UQ__users__F3DBC5723E209C51").IsUnique();

            entity.Property(e => e.created_date).HasDefaultValueSql("(getdate())");
            entity.Property(e => e.email).HasMaxLength(255);
            entity.Property(e => e.first_name).HasMaxLength(100);
            entity.Property(e => e.is_active).HasDefaultValue(true);
            entity.Property(e => e.last_name).HasMaxLength(100);
            entity.Property(e => e.password_hash).HasMaxLength(255);
            entity.Property(e => e.username).HasMaxLength(50);

            entity.HasOne(d => d.role).WithMany(p => p.users)
                .HasForeignKey(d => d.role_id)
                .OnDelete(DeleteBehavior.ClientSetNull)
                .HasConstraintName("FK_Users_Roles");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
