pub mod api_request;
pub mod format_stdout;
use regex::Regex;
use std::env;
use std::process::exit;

const API_TOKEN: &str = match option_env!("API_TOKEN") {
  Some(token) => token,
  None => "YOUR_API_TOKEN"
};


fn main() {
  let args: Vec<String> = env::args().collect();

  if args.len() < 3 {
    format_stdout::print_err("Usage: search-yt-pl -- <playlist_id> <search_keyword>");
    return;
  }

  let playlist_id = &args[1];
  let rest = &args[2..].join(" ");
  let search_keyword = rest.trim();

  let pattern = format!(r"(?i){}", regex::escape(search_keyword));
  let re = Regex::new(&pattern).unwrap();

  let mut page_token: Option<String> = None;
  let mut has_next_page = true;
  let mut page_count: i8 = 1;

  let mut all_videos: Vec<api_request::Snippet> = Vec::new();

  while has_next_page {
    let api_response = api_request::make_request(API_TOKEN, playlist_id, page_token.clone());

    match api_response {
      Ok(api_response) => {
        println!("Scanning page {}...", page_count);
        page_count += 1;

        // Filter videos based on search keyword and collect them
        all_videos.extend(
          api_response.items
          .into_iter()
          .filter_map(|item|
            if re.is_match(&item.snippet.title) {
              Some(item.snippet)
            }
            else { None })
        );

        match api_response.next_page_token {
          Some(token) => {
            page_token = Some(token)
          },
          None => {
            page_token = None;
            has_next_page = false;
          }
        }
      }
      Err(e) => {
        if e.is_status() {
          format_stdout::print_err(&format!("HTTP Error: {}", e.status().unwrap()));
          exit(1);
        }
        else {
          format_stdout::print_err(&format!("Error: {}", e));
        }
      }
    }
  }

  all_videos.iter().for_each(|video| {
    format_stdout::print_info(video, playlist_id);
  });
}
