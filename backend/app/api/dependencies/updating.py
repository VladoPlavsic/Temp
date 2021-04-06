from fastapi import Depends

from app.db.repositories.private.private import PrivateDBRepository
from app.cdn.repositories.private.private import PrivateYandexCDNRepository
from app.db.repositories.public.public import PublicDBRepository
from app.cdn.repositories.public.public import PublicYandexCDNRepository
from app.db.repositories.about.about import AboutDBRepository

from app.api.dependencies.database import get_db_repository
from app.api.dependencies.cdn import get_cdn_repository

async def update_sharing_links_function(
    public_db_repo: PublicDBRepository = Depends(get_db_repository(PublicDBRepository)),
    private_db_repo: PrivateDBRepository = Depends(get_db_repository(PrivateDBRepository)),
    about_db_repo: AboutDBRepository = Depends(get_db_repository(AboutDBRepository)),
    cdn_repo: PrivateYandexCDNRepository = Depends(get_cdn_repository(PrivateYandexCDNRepository)),
    ) -> None:

    # private content update
    grades = await private_db_repo.select_all_grades()
    if grades:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=grades, type_='structure')
        await private_db_repo.update_grade_links(grades=updated)

    subjects = await private_db_repo.select_all_subjects()
    if subjects:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=subjects, type_='structure')
        await private_db_repo.update_subject_links(subjects=updated)

    branches = await private_db_repo.select_all_branches()
    if branches:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=branches, type_='structure')
        await private_db_repo.update_branch_links(branches=updated)

    lectures = await private_db_repo.select_all_lectures()
    if lectures:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=lectures, type_='structure')
        await private_db_repo.update_lecture_links(lectures=updated)

    private_books = await private_db_repo.select_all_books()
    if private_books:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=lectures, type_='material')
        await private_db_repo.update_book_links(book=updated)

    private_theory_images = await private_db_repo.select_all_presentation_parts(presentation='theory', media_type='image')
    if private_theory_images:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=theory_images, type_='parts')
        await private_db_repo.update_presentation_part_links(prats=updated, presentation='theory', media_type='image')

    private_theory_audio = await private_db_repo.select_all_presentation_parts(presentation='theory', media_type='audio')
    if private_theory_audio:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=theory_audio, type_='parts')
        await private_db_repo.update_presentation_part_links(prats=updated, presentation='theory', media_type='audio')

    private_practice_images = await private_db_repo.select_all_presentation_parts(presentation='practice', media_type='image')
    if private_practice_images:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=practice_images, type_='parts')
        await private_db_repo.update_presentation_part_links(prats=updated, presentation='practice', media_type='image')

    private_practice_audio = await private_db_repo.select_all_presentation_parts(presentation='practice', media_type='audio')
    if private_practice_audio:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=practice_audio, type_='parts')
        await db_repo.update_presentation_part_links(prats=updated, presentation='practice', media_type='audio')

    # public content update
    public_books = await public_db_repo.select_all_books()
    if public_books:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_books, type_='material')
        await public_db_repo.update_book_links(book=updated)

    public_theory_images = await public_db_repo.select_all_presentation_parts(presentation='theory', media_type='image')
    if public_theory_images:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_theory_images, type_='parts')
        await public_db_repo.update_presentation_part_links(prats=updated, presentation='theory', media_type='image')

    public_theory_audio = await public_db_repo.select_all_presentation_parts(presentation='theory', media_type='audio')
    if public_theory_audio:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_theory_audio, type_='parts')
        await public_db_repo.update_presentation_part_links(prats=updated, presentation='theory', media_type='audio')
   
    public_practice_images = await public_db_repo.select_all_presentation_parts(presentation='practice', media_type='image')
    if public_practice_images:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_practice_images, type_='parts')
        await public_db_repo.update_presentation_part_links(prats=updated, presentation='practice', media_type='image')

    public_practice_audio = await public_db_repo.select_all_presentation_parts(presentation='practice', media_type='audio')
    if public_practice_audio:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=public_practice_audio, type_='parts')
        await public_db_repo.update_presentation_part_links(prats=updated, presentation='practice', media_type='audio')

    # about content update
    team_members = await about_db_repo.select_all_team_members()
    if team_members:
        updated = cdn_repo.get_sharing_links_from_objects(list_of_objects=team_members, type_='team')
        await about_db_repo.update_team_member_photos(photos=updated)