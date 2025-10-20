"""
Tests for the supplement optimization example.
"""

import os
import sys

import pytest

# Add the examples directory to the path so we can import supplement_optimizer
sys.path.append(
    os.path.join(
        os.path.dirname(__file__), "..", "..", "examples", "supplement_optimization"
    )
)

try:
    from supplement_optimizer import (
        DailyRequirement,
        Supplement,
        SupplementOptimizer,
        create_sample_data,
    )
except ImportError:
    # If running from a different location, try importing directly
    import supplement_optimizer

    Supplement = supplement_optimizer.Supplement
    DailyRequirement = supplement_optimizer.DailyRequirement
    SupplementOptimizer = supplement_optimizer.SupplementOptimizer
    create_sample_data = supplement_optimizer.create_sample_data


class TestSupplement:
    """Test the Supplement dataclass."""

    def test_supplement_creation(self):
        """Test creating a supplement with basic properties."""
        supp = Supplement(
            name="Test Vitamin",
            brand="TestBrand",
            form="tablet",
            nutrients={"Vitamin C": 100, "Calcium": 200},
            cost_per_unit=0.25,
        )

        assert supp.name == "Test Vitamin"
        assert supp.brand == "TestBrand"
        assert supp.form == "tablet"
        assert supp.nutrients["Vitamin C"] == 100
        assert supp.cost_per_unit == 0.25

    def test_supplement_string_representation(self):
        """Test the string representation of a supplement."""
        supp = Supplement(
            name="Multivitamin",
            brand="NatureMade",
            form="tablet",
            nutrients={"Vitamin C": 90},
        )

        assert str(supp) == "NatureMade Multivitamin (tablet)"


class TestDailyRequirement:
    """Test the DailyRequirement dataclass."""

    def test_daily_requirement_creation(self):
        """Test creating daily requirements."""
        req = DailyRequirement(
            age=30, gender="female", requirements={"Vitamin C": 75, "Calcium": 1000}
        )

        assert req.age == 30
        assert req.gender == "female"
        assert req.requirements["Vitamin C"] == 75

    def test_daily_requirement_string_representation(self):
        """Test the string representation of daily requirements."""
        req = DailyRequirement(age=25, gender="male", requirements={})

        assert str(req) == "Male, age 25"


class TestSupplementOptimizer:
    """Test the SupplementOptimizer class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.optimizer = SupplementOptimizer()

        # Create simple test supplements
        self.vitamin_c = Supplement(
            name="Vitamin C",
            brand="Test",
            form="tablet",
            nutrients={"Vitamin C": 100},
            cost_per_unit=0.10,
        )

        self.calcium = Supplement(
            name="Calcium",
            brand="Test",
            form="tablet",
            nutrients={"Calcium": 500},
            cost_per_unit=0.15,
        )

        self.multivitamin = Supplement(
            name="Multi",
            brand="Test",
            form="tablet",
            nutrients={"Vitamin C": 60, "Calcium": 200},
            cost_per_unit=0.20,
        )

        # Set up daily requirements
        self.daily_req = DailyRequirement(
            age=30, gender="female", requirements={"Vitamin C": 75, "Calcium": 1000}
        )

    def test_add_supplement(self):
        """Test adding supplements to the optimizer."""
        self.optimizer.add_supplement(self.vitamin_c)
        assert len(self.optimizer.supplements) == 1
        assert self.optimizer.supplements[0] == self.vitamin_c

    def test_set_daily_requirements(self):
        """Test setting daily requirements."""
        self.optimizer.set_daily_requirements(self.daily_req)
        assert self.optimizer.daily_req == self.daily_req

    def test_get_all_nutrients(self):
        """Test getting all unique nutrients."""
        self.optimizer.add_supplement(self.vitamin_c)
        self.optimizer.add_supplement(self.calcium)
        self.optimizer.set_daily_requirements(self.daily_req)

        nutrients = self.optimizer.get_all_nutrients()
        assert "Vitamin C" in nutrients
        assert "Calcium" in nutrients
        assert len(nutrients) == 2

    def test_create_nutritional_matrix(self):
        """Test creating the nutritional content matrix."""
        self.optimizer.add_supplement(self.vitamin_c)
        self.optimizer.add_supplement(self.calcium)
        self.optimizer.set_daily_requirements(self.daily_req)

        A, nutrients, supplement_names = self.optimizer.create_nutritional_matrix()

        # Check dimensions
        assert A.shape == (2, 2)  # 2 nutrients, 2 supplements

        # Check content
        vitamin_c_idx = supplement_names.index("Test Vitamin C (tablet)")
        calcium_idx = supplement_names.index("Test Calcium (tablet)")
        nutrient_c_idx = nutrients.index("Vitamin C")
        nutrient_ca_idx = nutrients.index("Calcium")

        assert A[nutrient_c_idx, vitamin_c_idx] == 100  # Vitamin C has 100mg Vitamin C
        assert A[nutrient_ca_idx, calcium_idx] == 500  # Calcium has 500mg Calcium
        assert A[nutrient_ca_idx, vitamin_c_idx] == 0  # Vitamin C has 0mg Calcium

    def test_solve_minimum_pills_simple(self):
        """Test solving for minimum pills with a simple case."""
        self.optimizer.add_supplement(self.vitamin_c)
        self.optimizer.add_supplement(self.calcium)
        self.optimizer.set_daily_requirements(self.daily_req)

        result = self.optimizer.solve_minimum_pills()

        assert result["success"] is True
        assert result["total_pills"] > 0
        assert len(result["supplement_plan"]) > 0
        assert len(result["nutrient_analysis"]) == 2

    def test_solve_minimum_cost(self):
        """Test solving for minimum cost."""
        self.optimizer.add_supplement(self.vitamin_c)
        self.optimizer.add_supplement(self.calcium)
        self.optimizer.set_daily_requirements(self.daily_req)

        result = self.optimizer.solve_minimum_cost()

        assert result["success"] is True
        assert "total_cost" in result
        assert result["total_cost"] > 0

    def test_error_handling_no_supplements(self):
        """Test error handling when no supplements are added."""
        self.optimizer.set_daily_requirements(self.daily_req)

        with pytest.raises(ValueError, match="No supplements added"):
            self.optimizer.solve_minimum_pills()

    def test_error_handling_no_requirements(self):
        """Test error handling when no requirements are set."""
        self.optimizer.add_supplement(self.vitamin_c)

        with pytest.raises(ValueError, match="Daily requirements not set"):
            self.optimizer.solve_minimum_pills()

    def test_integer_solution(self):
        """Test integer solution (whole pills only)."""
        self.optimizer.add_supplement(self.vitamin_c)
        self.optimizer.add_supplement(self.calcium)
        self.optimizer.set_daily_requirements(self.daily_req)

        result = self.optimizer.solve_minimum_pills(allow_fractional=False)

        assert result["success"] is True

        # Check that all quantities are integers
        for item in result["supplement_plan"]:
            assert item["quantity"] == int(item["quantity"])


class TestSampleData:
    """Test the sample data creation function."""

    def test_create_sample_data(self):
        """Test that sample data is created correctly."""
        supplements, daily_req = create_sample_data()

        assert len(supplements) > 0
        assert isinstance(daily_req, DailyRequirement)

        # Check that all supplements have the required attributes
        for supp in supplements:
            assert hasattr(supp, "name")
            assert hasattr(supp, "brand")
            assert hasattr(supp, "form")
            assert hasattr(supp, "nutrients")
            assert hasattr(supp, "cost_per_unit")

        # Check daily requirements
        assert daily_req.age > 0
        assert daily_req.gender in ["male", "female"]
        assert len(daily_req.requirements) > 0


class TestIntegration:
    """Integration tests using the sample data."""

    def test_full_optimization_workflow(self):
        """Test the complete optimization workflow with sample data."""
        supplements, daily_req = create_sample_data()

        optimizer = SupplementOptimizer()
        optimizer.set_daily_requirements(daily_req)

        for supplement in supplements:
            optimizer.add_supplement(supplement)

        # Test minimum pills
        result_pills = optimizer.solve_minimum_pills()
        assert result_pills["success"] is True

        # Test minimum cost
        result_cost = optimizer.solve_minimum_cost()
        assert result_cost["success"] is True

        # Test integer solution
        result_integer = optimizer.solve_minimum_pills(allow_fractional=False)
        assert result_integer["success"] is True

        # Integer solution should have higher or equal pill count
        assert result_integer["total_pills"] >= result_pills["total_pills"]


if __name__ == "__main__":
    pytest.main([__file__])
