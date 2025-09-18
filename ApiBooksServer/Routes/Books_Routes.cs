using Microsoft.AspNetCore.Mvc;

namespace ApiBooksServer.Routes;

[ApiController]
[Route("api/books")]
public class BooksRoutes : ControllerBase
{
    [HttpGet("/detait/{id?}")]
    public IActionResult DetailBooks(int? id)
    {
        return Ok($"Вывод подробной информации о книге: {id}");
    }

    [HttpGet("{idGenge?}/{name?}")]
    public IActionResult WriteLineBooks(int? idGenge, string? name)
    {
        return Ok($"Вывод книг по жанру: {idGenge}, названию: {name}");
    }

    [HttpGet("/read/{id}")]
    public IActionResult ReadBook(int id)
    {
        return Ok($"Вывод чтение книги: {id}");
    }
}