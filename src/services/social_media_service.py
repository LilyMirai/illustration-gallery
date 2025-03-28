class SocialMediaService:
    def __init__(self):
        pass

    def format_post(self, illustration):
        post_content = f"Check out my latest illustration: {illustration.title}\n"
        post_content += f"Description: {illustration.description}\n"
        post_content += f"Tags: {', '.join(illustration.tags)}\n"
        post_content += f"Progress: {illustration.progress_state}\n"
        return post_content

    def generate_social_media_links(self, illustration):
        links = {
            "Twitter": f"https://twitter.com/intent/tweet?text={self.format_post(illustration)}",
            "Facebook": f"https://www.facebook.com/sharer/sharer.php?u={illustration.image_url}",
            "Instagram": f"https://www.instagram.com/create/story/?media={illustration.image_url}"
        }
        return links