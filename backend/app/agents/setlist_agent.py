"""AI agent for DJ setlist generation using Qwen/LLM API."""

import json
import logging
from openai import AsyncOpenAI
from app.core.config import settings
from app.models.models import Track

logger = logging.getLogger(__name__)

# Initialize OpenAI-compatible client for Qwen API
client = AsyncOpenAI(
    api_key=settings.LLM_API_KEY,
    base_url=settings.LLM_API_BASE_URL,
)


def _format_track_for_prompt(track: Track) -> str:
    """Format track data for LLM prompt."""
    return (
        f"- {track.title} by {track.artist} | "
        f"BPM: {track.bpm} | Key: {track.key} | "
        f"Energy: {track.energy_level}/10"
        + (f" | Genre: {track.genre}" if track.genre else "")
        + (f" | Duration: {track.duration_seconds:.0f}s" if track.duration_seconds else "")
    )


async def generate_setlist_with_ai(
    tracks: list[Track],
    target_duration_minutes: int | None = None,
    vibe: str | None = None,
    starting_track_id: str | None = None,
    max_tracks: int | None = None,
) -> dict:
    """Generate an optimized DJ setlist using AI analysis."""
    # Format tracks for prompt
    tracks_text = "\n".join([_format_track_for_prompt(t) for t in tracks])
    
    duration_text = f"\nTarget duration: {target_duration_minutes} minutes" if target_duration_minutes else ""
    vibe_text = f"\nVibe/Style: {vibe}" if vibe else ""
    max_text = f"\nMaximum tracks in setlist: {max_tracks}" if max_tracks else ""
    
    prompt = f"""You are an expert DJ setlist generator. Analyze the following tracks and create an optimal setlist.

Available tracks:
{tracks_text}
{duration_text}{vibe_text}{max_text}

Rules for seamless DJ mixing:
1. Match BPM within ±5-8 BPM for smooth transitions
2. Use Camelot Wheel for harmonic mixing (compatible keys are: same number +/-1, same letter OR same number, A<->B)
3. Build energy gradually (1-10 scale)
4. Consider genre compatibility
5. Create a natural flow and journey

Respond with ONLY a valid JSON object in this exact format:
{{
  "track_order": [
    {{"track_id": "id1", "position": 1, "transition_notes": "Why this track works here"}},
    {{"track_id": "id2", "position": 2, "transition_notes": "..."}}
  ],
  "ai_notes": "Overall explanation of the setlist strategy and flow",
  "suggestions": ["Tip 1", "Tip 2"],
  "compatibility_scores": {{"id1->id2": 0.95}}
}}

Order tracks logically and explain your reasoning."""

    try:
        response = await client.chat.completions.create(
            model=settings.LLM_API_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional DJ setlist generator. Always respond with valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=4000,
        )
        
        # Parse response
        content = response.choices[0].message.content.strip()
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
        if content.startswith("json"):
            content = content[4:].lstrip()
        
        result = json.loads(content)
        return result
        
    except Exception as e:
        logger.error(f"AI setlist generation failed: {e}")
        # Fallback to algorithmic approach
        return _algorithmic_setlist(tracks, target_duration_minutes, vibe, max_tracks)


async def recommend_next_track(
    current_track: Track,
    available_tracks: list[Track],
) -> dict:
    """Get AI recommendation for the next track to play."""
    current_text = _format_track_for_prompt(current_track)
    available_text = "\n".join([_format_track_for_prompt(t) for t in available_tracks])
    
    prompt = f"""Current playing track:
{current_text}

Available next tracks:
{available_text}

As an expert DJ, recommend the best next track for a seamless transition. Consider:
1. BPM matching (within ±8 BPM ideal)
2. Harmonic compatibility (Camelot Wheel rules)
3. Energy flow (should build or maintain appropriately)
4. Genre consistency

Respond with ONLY a valid JSON object:
{{
  "track_id": "recommended_track_id",
  "reasoning": "Why this track is the best choice",
  "compatibility_score": 0.92,
  "transition_tips": "Specific mixing tips for this transition"
}}"""

    try:
        response = await client.chat.completions.create(
            model=settings.LLM_API_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional DJ. Always respond with valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=1000,
        )
        
        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
        if content.startswith("json"):
            content = content[4:].lstrip()
        
        result = json.loads(content)
        
        # Find the recommended track
        recommended = next((t for t in available_tracks if t.id == result["track_id"]), available_tracks[0])
        
        return {
            "recommended_track": recommended,
            "reasoning": result.get("reasoning", "AI recommendation based on compatibility"),
            "compatibility_score": result.get("compatibility_score", 0.8),
            "transition_tips": result.get("transition_tips", "Mix on phrase boundaries"),
        }
        
    except Exception as e:
        logger.error(f"AI recommendation failed: {e}")
        # Fallback to algorithmic
        return _algorithmic_next_track(current_track, available_tracks)


def _algorithmic_setlist(
    tracks: list[Track],
    target_duration_minutes: int | None,
    vibe: str | None,
    max_tracks: int | None,
) -> dict:
    """Fallback algorithmic setlist generation."""
    # Sort by energy level for natural progression
    sorted_tracks = sorted(tracks, key=lambda t: (t.energy_level, t.bpm))
    
    if max_tracks:
        sorted_tracks = sorted_tracks[:max_tracks]
    
    track_order = [
        {"track_id": t.id, "position": i + 1, "transition_notes": f"Energy level {t.energy_level}, BPM {t.bpm}"}
        for i, t in enumerate(sorted_tracks)
    ]
    
    return {
        "track_order": track_order,
        "ai_notes": "Algorithmic fallback: sorted by energy and BPM progression",
        "suggestions": ["Try AI generation for better results with LLM"],
        "compatibility_scores": {},
    }


def _algorithmic_next_track(current_track: Track, available_tracks: list[Track]) -> dict:
    """Fallback algorithmic next track recommendation."""
    best_score = -1
    best_track = available_tracks[0]
    
    for track in available_tracks:
        score = 0
        # BPM proximity
        bpm_diff = abs(track.bpm - current_track.bpm)
        score += max(0, 10 - bpm_diff)
        # Energy progression
        energy_diff = track.energy_level - current_track.energy_level
        score += max(0, 5 - abs(energy_diff - 1))  # Prefer +1 energy
        # Key compatibility (simplified Camelot)
        if track.key == current_track.key:
            score += 10
        
        if score > best_score:
            best_score = score
            best_track = track
    
    return {
        "recommended_track": best_track,
        "reasoning": f"Best match: BPM diff {abs(best_track.bpm - current_track.bpm):.1f}, energy {best_track.energy_level}",
        "compatibility_score": min(1.0, best_score / 20),
        "transition_tips": "Match beats and mix on phrase boundaries",
    }
