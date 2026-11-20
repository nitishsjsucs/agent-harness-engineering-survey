# Video presentation

**YouTube:** <!--YOUTUBE-->link added after upload<!--/YOUTUBE-->
**File in this repo:** `video/short_story_presentation.mp4` (added after recording)

The talk walks through the 27 slides in [`../slides/harness_short_story.pptx`](../slides/harness_short_story.pptx). The word-for-word narration, with a start time for every slide, is in [`presentation_script.md`](presentation_script.md). The same text is in each slide's speaker notes.

| | |
|---|---|
| Slides | 27 |
| Narration | about 2,100 words |
| Expected length | about 16 min at 150 wpm, 17.5 min at 135 wpm |
| Target | at least 15:00 (YouTube requirement), so keep a relaxed pace |

## Recording (pick one)

**Zoom (the brief suggests it).** Start a meeting with only yourself, share the PowerPoint or Keynote window in slideshow mode, turn your camera on if you want a corner video, and click *Record → Record on this computer*. Zoom saves an MP4 when the meeting ends.

**Keynote.** Open the `.pptx` in Keynote and choose *Play → Record Slideshow*. You narrate while advancing slides, then use *File → Export To → Movie*.

**PowerPoint.** *Slide Show → Record*, then *File → Export → Create a Video* (1080p).

**QuickTime.** *File → New Screen Recording*, choose the microphone under Options, and record the slideshow window.

Tips:

- Keep the speaker notes open on a second screen (Presenter View) and read naturally rather than word for word.
- Check the timer at slide 14 (the ablation slide): you should be around 9 minutes in.
- If you finish early, expand on the "two cents" slides. That is where your own view counts most.

## Compress and add to the repo

GitHub rejects files over 100 MB. Slides compress very well:

```bash
bash tools/compress_video.sh ~/Desktop/recording.mp4
git add video/short_story_presentation.mp4 && git commit -m "Add presentation video" && git push
```

The script writes `video/short_story_presentation.mp4` at 720p and warns you if the file is still over 95 MB or if the video is shorter than 15 minutes.

## Upload to YouTube

1. Go to studio.youtube.com, click *Create → Upload videos*, and upload the full-quality recording (not the compressed one).
2. Title: *The Harness Is Half the Agent: four 2026 surveys on LLM agent harness engineering*.
3. Description: paste the four arXiv links and the GitHub URL.
4. Visibility: Public or Unlisted (check what the course allows).
5. Put the link into the repo:

   ```bash
   python3 tools/update_links.py --youtube https://youtu.be/<id>
   ```
