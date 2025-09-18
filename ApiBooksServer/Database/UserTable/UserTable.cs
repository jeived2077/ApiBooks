
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations;
using ApiBooksServer.Database.LikeBooksUser;
using Microsoft.EntityFrameworkCore;

namespace ApiBooksServer.Database.UserTable;

public class UserTable
{
   [Key]
   public int UserId { get; set; } 
   public string FirstName { get; set; }
   public string LastName { get; set; }
   public string Email { get; set; }
   public string Hashing_Password { get; set; }
   public string Hashing_Salt { get; set; }
   public Byte Avatar { get; set; }
   public List<LikeBooksUserTable> UserLikes { get; set; } = new();
}