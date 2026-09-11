import pytest
from expense_tracker.services.category_service import CategoryService, DuplicateCategoryError


class TestCategoryService:
    def test_list_categories(self, temp_db):
        cat_service = CategoryService()
        categories = cat_service.list_categories()
        cat_service.close()
        assert len(categories) >= 8
        category_names = [cat.name for cat in categories]
        assert "Food" in category_names
        assert "Transport" in category_names

    def test_get_category(self, temp_db):
        cat_service = CategoryService()
        cat = cat_service.get_category(1)
        cat_service.close()
        assert cat is not None
        assert cat.id == 1
        assert cat.name == "Food"

    def test_get_category_by_name(self, temp_db):
        cat_service = CategoryService()
        cat = cat_service.get_category_by_name("Food")
        cat_service.close()
        assert cat is not None
        assert cat.name == "Food"

    def test_get_category_not_found(self, temp_db):
        cat_service = CategoryService()
        cat = cat_service.get_category(999)
        cat_service.close()
        assert cat is None

    def test_get_category_by_name_not_found(self, temp_db):
        cat_service = CategoryService()
        cat = cat_service.get_category_by_name("NonExistent")
        cat_service.close()
        assert cat is None

    def test_add_category(self, temp_db):
        cat_service = CategoryService()
        cat_id = cat_service.add_category("Gym")
        cat_service.close()
        assert cat_id is not None

    def test_add_category_duplicate(self, temp_db):
        cat_service = CategoryService()
        cat_service.add_category("Gym")
        with pytest.raises(DuplicateCategoryError):
            cat_service.add_category("Gym")
        cat_service.close()

    def test_add_category_default_duplicate(self, temp_db):
        cat_service = CategoryService()
        with pytest.raises(DuplicateCategoryError):
            cat_service.add_category("Food")
        cat_service.close()

    def test_delete_category(self, temp_db):
        cat_service = CategoryService()
        cat_id = cat_service.add_category("Temporary")
        result = cat_service.delete_category(cat_id)
        cat_service.close()
        assert result is True

    def test_delete_category_not_found(self, temp_db):
        cat_service = CategoryService()
        result = cat_service.delete_category(999)
        cat_service.close()
        assert result is False