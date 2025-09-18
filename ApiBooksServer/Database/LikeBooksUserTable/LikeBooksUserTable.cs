using ApiBooksServer.Database.BooksTable;
using ApiBooksServer.Database.UserTable;
using System;

namespace ApiBooksServer.Database.LikeBooksUser;

public class LikeBooksUserTable
{
    
    public int UserId { get; set; }

    
    public UserTable.UserTable User { get; set; } = null!;

   
    public int BookId { get; set; }

    
    public BooksTable.BooksTable Book { get; set; } = null!;

    public DateTime DateLiked { get; set; } = DateTime.Now;
}