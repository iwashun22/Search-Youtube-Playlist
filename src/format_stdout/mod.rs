use crate::api_request;
use colored::ColoredString;
use colored::Colorize;

fn colored_str(s: &str, color_code: u8) -> ColoredString {
  s.ansi_color(color_code)
}

pub fn print_err(e: &str) {
  eprintln!("{}", colored_str(e, 160));
}

struct KeyValue {
  key: ColoredString,
  context: ColoredString
}

pub fn print_info(video: &api_request::Snippet, playlist_id: &str) {
  let title: KeyValue = KeyValue {
    key: colored_str("Title:", 34).bold(),
    context: colored_str(&video.title, 112)
  };

  let description: KeyValue = KeyValue {
    key: colored_str("Description:", 93).bold(),
    context: colored_str(&video.description, 62)
  };

  let formatted_url = format!("https://www.youtube.com/watch?v={}&list={}", video.resource_id.video_id, playlist_id);
  let url: KeyValue = KeyValue {
    key: colored_str("Link:", 201).bold(),
    context: colored_str(&formatted_url, 33)
  };

  println!("\n\n");
  [title, description, url].iter().for_each(|kv| {
    println!("{} {}", kv.key, kv.context);
  });
  println!("{}", colored_str("-----------------------------", 19));
}
