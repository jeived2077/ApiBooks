using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ApiBooksServer.Database.BooksTable;

public class BooksTable
{
    [Key]
    public int BookId { get; set; }
    public string BookName { get; set; }
    public int YearCreate { get; set; }
    [ForeignKey("GenreTable")]
    public int GenreId  { get; set; };
    public int SaledBooks { get; set; }
    public byte[] ImageBooks { get; set; }
    public string Description { get; set; }
    public virtual GenreTable.GenreTable Genre { get; set; }
}