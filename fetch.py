from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter, JSONFormatter
import srt


def generate_subtitle(en_sub, other_sub, language):
    en_generator = srt.parse(en_sub)
    other_generator = srt.parse(other_sub)
    en_list = list(en_generator)
    other_list = list(other_generator)
    en_duplicate = en_list.copy()
    line_number = 0
    for line in en_duplicate:
        duelText = line.content + "\n"
        try:
            append = other_list[line_number].content
            duelText += append
            line.content = duelText
        except IndexError:
            print('Error language: ', language)
            break
        line_number += 1
    write_to_file(language + '_dual.srt', en_duplicate)


def write_to_file(file_name, string):
    # write it out to a file
    with open(file_name, 'w', encoding='utf-8') as srt_file:
        subtitle = srt.compose(string)
        srt_file.write(subtitle)
        srt_file.close()


def main():
    video_id = 'R7MdvMLz6Qo'
    # foreign transcript
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    srt_formatter = SRTFormatter()
    # english transcript
    get_transcript = YouTubeTranscriptApi.get_transcript(video_id)
    en = srt_formatter.format_transcript(get_transcript)
    with open('en' + '_single.srt', 'w', encoding='utf-8') as srt_file:
        srt_file.write(en)

    language_list = {'de', 'fr', 'es', 'zh-Hans'}
    for language in language_list:
        find_transcript = transcript_list.find_transcript(['en'])
        translated_transcript = find_transcript.translate(language)
        # zh-Hans_translated
        fetched_translated = translated_transcript.fetch()
        other = srt_formatter.format_transcript(fetched_translated)
        generate_subtitle(en, other, language)

        with open(language + '_single.srt', 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_formatter.format_transcript(fetched_translated))



if __name__ == '__main__':
    main()
