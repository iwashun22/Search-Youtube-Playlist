use reqwest::blocking::Client;
use reqwest::Error;
pub mod api_response;
pub use api_response::ApiResponse;
pub use api_response::Snippet;

#[derive(serde::Serialize)]
struct Query {
  part: String,
  #[serde(rename = "playlistId")]
  playlist_id: String,
  #[serde(rename = "maxResult")]
  max_result: i8,
  key: String,
  #[serde(rename = "pageToken")]
  page_token: String
}


pub fn make_request(api_token: &str, playlist_id: &str, page_token: Option<String>) -> Result<ApiResponse, Error> {
  let params = Query {
    part: "snippet".to_string(),
    playlist_id: playlist_id.to_string(),
    max_result: 50,
    key: api_token.to_string(),
    page_token: page_token.unwrap_or_default()
  };

  let client = Client::new();

  let query_string = serde_urlencoded::to_string(&params).unwrap();
  let url = format!("https://www.googleapis.com/youtube/v3/playlistItems?{}", query_string);

  let response = client.get(&url).send()?.error_for_status()?;
  let api_response = response.json::<ApiResponse>().unwrap();

  Ok(api_response)
}