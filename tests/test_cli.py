from clarity.cli import main


def test_cli_displays_a_malformed_source_error(tmp_path, capsys):
    source = tmp_path / "broken.clr"
    source.write_text('say "unfinished\\', encoding="utf-8")

    assert main([str(source)]) == 1
    output = capsys.readouterr().out
    assert "Clarity Lexer Error" in output
    assert "escape sequence is incomplete" in output
    assert "Line 1, column 5" in output
