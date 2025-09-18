
using System.ComponentModel.DataAnnotations;
using Microsoft.EntityFrameworkCore;
namespace ApiBooksServer.Database.GenreTable;

public class GenreTable
{
    [Key]
    public int GenreId { get; set; }
    public string GenreName { get; set; }
    public virtual ICollection<BooksTable.BooksTable> Books { get; set; }
}
