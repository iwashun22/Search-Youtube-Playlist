use serde::Deserialize;

#[derive(Deserialize, Debug)]
pub struct ApiResponse {
  #[serde(rename = "nextPageToken")]
  pub next_page_token: Option<String>,
  pub items: Vec<PlaylistItem>
}

#[derive(Deserialize, Debug)]
pub struct PlaylistItem {
  pub snippet: Snippet
}

#[derive(Deserialize, Debug)]
pub struct Snippet {
  pub title: String,
  pub description: String,
  #[serde(rename = "resourceId")]
  pub resource_id: ResourceId
}

#[derive(Deserialize, Debug)]
pub struct ResourceId {
  #[serde(rename = "videoId")]
  pub video_id: String
}
