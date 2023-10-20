import scrapy


def collect_blocked_images(response, current_thread_page):
    print("##########################")
    print("collect_blocked_images has been called")
    items = []
    for link in response.xpath('//a'):
        text = link.xpath('text()').get()
        href = link.xpath('@href').get()

        if text and "[Image:" in text:
            item = {
                'text': text,
                'href': href,
                'page_url': response.url,
                'pagination_current': current_thread_page
            }
            items.append(item)
    return items


class ForumSpider(scrapy.Spider):
    name = 'eaglespider'
    start_urls = ['https://eagle-time.org/showthread.php?tid=1062&page=1']

    def parse(self, response, **kwargs):
        current_url = response.url
        # confirm that you are in a thread
        thread_index = current_url.find("tid=")
        if thread_index == -1:
            print("##########################")
            print("You are not in a thread.")
            print("current_url: " + current_url)
            # not in a thread, do nothing
            return
        # check if thread has multiple pages
        if response.css("span.pagination_current"):
            # extra pages exist
            current_page = response.css("span.pagination_current::text").get()
            # check if current_page matches page value in current_url
            index_page = current_url.find("&page=")
            if index_page == -1:
                print("##########################")
                print("Something is wrong.")
                print("current_url: " + current_url)
                # no "&page=" in current_url, but pagination_current exists. Something is wrong.
                return
            if current_page != current_url[index_page + 6:]:
                print("##########################")
                print("You are on the wrong page. Perhaps you revisited the start")
                print("current_url: " + current_url)
                print("current_page: " + current_page)
                # current_page does not match page value in current_url
                # you are on the wrong page this should only happen when current_page is 1
                # and the page value in current_url has exceeded the number of actual pages
                return
            # You are on the correct page, collect the data, then advance to the next page.
            print("##########################")
            print("Multiple Pages detected")

            yield from collect_blocked_images(response, current_page)

            next_page_url = current_url[:index_page + 6] + str(int(current_page) + 1)
            print("next_page_url: " + next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            # no extra pages exist
            # collect the data
            print("##########################")
            print("No extra pages detected")
            yield from collect_blocked_images(response, 1)
