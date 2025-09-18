using ApiBooksServer.Database.AuthorTable;
using ApiBooksServer.Database.BooksTable;
using ApiBooksServer.Database.GenreTable;
using ApiBooksServer.Database.LikeBooksUser;
using ApiBooksServer.Database.UserTable;

namespace ApiBooksServer.EfCore;

using Microsoft.EntityFrameworkCore;
public class ApplicationContext : DbContext
{
    public DbSet<UserTable> Users { get; set; } = null!;
    public DbSet<BooksTable> Books { get; set; } = null!;
    public DbSet<GenreTable> Genres { get; set; } = null!;
    public DbSet<AuthorTable> Authors { get; set; } = null!;
    public DbSet<LikeBooksUserTable>  LikeBooksUsers { get; set; } = null!;
    public ApplicationContext(DbContextOptions<ApplicationContext> options)
        : base(options)
    {
        Database.EnsureCreated();   
    }
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<UserTable>().ToTable("User");
        modelBuilder.Entity<BooksTable>()
            .HasOne(b => b.Genre) 
            .WithMany(g => g.Books) 
            .HasForeignKey(b => b.GenreId);
        modelBuilder.Entity<GenreTable>().ToTable("Genre");
        
        
        
    }

    
}