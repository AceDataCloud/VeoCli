"""Video generation commands."""

import click

from veo_cli.core.client import get_client
from veo_cli.core.exceptions import VeoError
from veo_cli.core.output import (
    VEO_MODELS, DEFAULT_MODEL, print_error, print_json, print_video_result, ASPECT_RATIOS, DEFAULT_ASPECT_RATIO,
)


@click.command()
@click.argument("prompt")
@click.option(
    "-m",
    "--model",
    type=click.Choice(VEO_MODELS),
    default=DEFAULT_MODEL,
    help="Veo model version.",
)
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    help="Aspect ratio of the output.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def generate(
    ctx: click.Context,
    prompt: str,
    model: str,
    aspect_ratio: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from a text prompt.

    PROMPT is a detailed description of what to generate.

    Examples:

      veo generate "A cinematic scene of a sunset over the ocean"

      veo generate "A cat playing with yarn" -m veo3
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "prompt": prompt,
            "model": model,
            "callback_url": callback_url,
            "aspect_ratio": aspect_ratio,
        }

        result = client.generate_video(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command("image-to-video")
@click.argument("prompt")
@click.option(
    "-i",
    "--image-url",
    "image_urls",
    required=True,
    multiple=True,
    help="Image URL(s) for reference. Can be specified multiple times.",
)
@click.option(
    "-m",
    "--model",
    type=click.Choice(VEO_MODELS),
    default=DEFAULT_MODEL,
    help="Veo model version.",
)
@click.option(
    "-a",
    "--aspect-ratio",
    type=click.Choice(ASPECT_RATIOS),
    default=DEFAULT_ASPECT_RATIO,
    help="Aspect ratio of the output.",
)
@click.option("--callback-url", default=None, help="Webhook callback URL.")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def image_to_video(
    ctx: click.Context,
    prompt: str,
    image_urls: tuple[str, ...],
    model: str,
    aspect_ratio: str,
    callback_url: str | None,
    output_json: bool,
) -> None:
    """Generate a video from reference image(s).

    PROMPT describes the desired video. Provide one or more image URLs as reference.

    Examples:

      veo image-to-video "Animate this scene" -i https://example.com/photo.jpg

      veo image-to-video "Bring to life" -i img1.jpg -i img2.jpg
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.generate_video(
            prompt=prompt,
            image_urls=list(image_urls),
            model=model,
            aspect_ratio=aspect_ratio,
            callback_url=callback_url,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e


@click.command()
@click.argument("video_id")
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def upscale(
    ctx: click.Context,
    video_id: str,
    output_json: bool,
) -> None:
    """Get 1080p version of a generated video.

    VIDEO_ID is the ID of the video to upscale.

    Examples:

      veo upscale abc123-def456
    """
    client = get_client(ctx.obj.get("token"))
    try:
        result = client.upscale_video(
            video_id=video_id,
        )
        if output_json:
            print_json(result)
        else:
            print_video_result(result)
    except VeoError as e:
        print_error(e.message)
        raise SystemExit(1) from e

