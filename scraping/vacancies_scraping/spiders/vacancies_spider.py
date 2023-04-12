from typing import Generator

import scrapy
from scrapy.http import Response

from vacancies_scraping.items import Vacancy


class VacancySpider(scrapy.Spider):
    name = "vacancies"
    base_jobs_url = "https://djinni.co"
    base_pages_url = "https://djinni.co/jobs/"

    def start_requests(self) -> Generator:
        start_url = 'https://djinni.co/jobs/?primary_keyword=Python'
        yield scrapy.Request(
            url=start_url,
            callback=self.get_vacancies_links_from_page
        )

    def get_vacancies_links_from_page(self, response: Response) -> Generator:
        for vacancy_url in response.css("a.profile::attr(href)").getall():
            yield response.follow(
                self.base_jobs_url + vacancy_url,
                callback=self.parse
            )

        next_page_disabled = bool(
            response.css(".pagination > li > a.page-link")[-1].xpath("@aria-disabled")
        )

        if not next_page_disabled:
            next_page_path = response.css(
                ".pagination > li > a.page-link::attr(href)"
            ).getall()[-1]

            yield response.follow(
                self.base_pages_url + next_page_path,
                callback=self.get_vacancies_links_from_page
            )

    def parse(self, response: Response, **kwargs) -> Vacancy:
        company = response.css("a.job-details--title::text").get().strip()
        applications = int(response.css("p.text-muted").re(r"(\d+) відгук")[0])
        views = int(response.css("p.text-muted").re(r"(\d+) перегляд")[0])
        experience = response.css(".job-additional-info--body")[0].css(
            ".job-additional-info--item-text::text"
        ).getall()[-1].strip().split()[0]

        if experience == "Без":
            experience = 0
        else:
            experience = int(experience)

        salary = response.css(".detail--title-wrapper .public-salary-item").getall()

        if salary:
            salary = int(response.css(".detail--title-wrapper .public-salary-item").re(r"\$(\d+)")[0])
        else:
            salary = None

        tags = response.css(".job-additional-info--body")[0].css(
            ".job-additional-info--item-text span::text"
        ).getall()

        if not tags:
            tags = None

        yield Vacancy(
            company=company,
            tags=tags,
            experience=experience,
            salary=salary,
            views=views,
            applications=applications
        )
