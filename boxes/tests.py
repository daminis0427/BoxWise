
from decimal import Decimal

from django.test import TestCase

from .models import Product, ShippingBox, Order, OrderItem
from .services import (
    get_orientations,
    fits_in_space,
    pack_products,
    get_suitable_boxes,
    recommend_box,
    get_cost_savings,
)


class BoxWiseModelTests(TestCase):

    def test_create_product(self):
        product = Product.objects.create(
            name="Laptop",
            length=5,
            width=4,
            height=2,
            weight=2,
        )

        self.assertEqual(product.name, "Laptop")
        self.assertEqual(str(product), "Laptop")

    def test_create_shipping_box(self):
        box = ShippingBox.objects.create(
            name="Small Box",
            length=10,
            width=10,
            height=10,
            max_weight=20,
            cost=Decimal("50.00"),
        )

        self.assertEqual(box.name, "Small Box")
        self.assertEqual(box.cost, Decimal("50.00"))


class BoxWisePackingTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Laptop",
            length=5,
            width=2,
            height=1,
            weight=2,
        )

        self.order = Order.objects.create()

        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
        )

        self.box = ShippingBox.objects.create(
            name="Large Box",
            length=10,
            width=10,
            height=10,
            max_weight=20,
            cost=Decimal("50.00"),
        )

    def test_product_orientations(self):
        orientations = get_orientations(self.product)

        self.assertIn((5, 2, 1), orientations)
        self.assertIn((1, 5, 2), orientations)

    def test_product_fits_in_space(self):
        result = fits_in_space(
            (2, 3, 4),
            (5, 5, 5),
        )

        self.assertTrue(result)

    def test_product_does_not_fit_in_space(self):
        result = fits_in_space(
            (6, 3, 4),
            (5, 5, 5),
        )

        self.assertFalse(result)

    def test_successful_product_packing(self):
        placements = pack_products(
            [self.order_item],
            self.box,
        )

        self.assertIsNotNone(placements)
        self.assertEqual(len(placements), 1)
        self.assertEqual(
            placements[0]["name"],
            "Laptop",
        )
        self.assertIn("color", placements[0])

    def test_product_rotation_during_packing(self):
        rotation_box = ShippingBox.objects.create(
            name="Rotated Box",
            length=1,
            width=5,
            height=2,
            max_weight=20,
            cost=Decimal("30.00"),
        )

        placements = pack_products(
            [self.order_item],
            rotation_box,
        )

        self.assertIsNotNone(placements)
        self.assertEqual(len(placements), 1)

    def test_packing_fails_when_product_is_too_large(self):
        small_box = ShippingBox.objects.create(
            name="Tiny Box",
            length=1,
            width=1,
            height=1,
            max_weight=20,
            cost=Decimal("10.00"),
        )

        placements = pack_products(
            [self.order_item],
            small_box,
        )

        self.assertIsNone(placements)

    def test_packing_with_no_box(self):
        placements = pack_products(
            [self.order_item],
            None,
        )

        self.assertIsNone(placements)

    def test_packing_empty_order_items(self):
        placements = pack_products([], self.box)

        self.assertEqual(placements, [])

    def test_quantity_expands_into_individual_products(self):
        self.order_item.quantity = 2
        self.order_item.save()

        placements = pack_products(
            [self.order_item],
            self.box,
        )

        self.assertEqual(len(placements), 2)


class BoxWiseRecommendationTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Book",
            length=2,
            width=2,
            height=2,
            weight=1,
        )

        self.order = Order.objects.create()

        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
        )

        self.cheap_box = ShippingBox.objects.create(
            name="Cheap Box",
            length=5,
            width=5,
            height=5,
            max_weight=10,
            cost=Decimal("20.00"),
        )

        self.expensive_box = ShippingBox.objects.create(
            name="Expensive Box",
            length=10,
            width=10,
            height=10,
            max_weight=10,
            cost=Decimal("40.00"),
        )

        self.light_box = ShippingBox.objects.create(
            name="Low Weight Box",
            length=5,
            width=5,
            height=5,
            max_weight=0.5,
            cost=Decimal("5.00"),
        )

    def test_get_suitable_boxes(self):
        suitable_boxes = get_suitable_boxes(self.order)

        self.assertEqual(len(suitable_boxes), 2)
        self.assertNotIn(self.light_box, suitable_boxes)

    def test_recommend_cheapest_suitable_box(self):
        recommended = recommend_box(self.order)

        self.assertEqual(recommended, self.cheap_box)

    def test_no_recommendation_when_no_box_is_suitable(self):
        ShippingBox.objects.all().delete()

        recommended = recommend_box(self.order)

        self.assertIsNone(recommended)

    def test_cost_savings_calculation(self):
        result = get_cost_savings(self.order)

        self.assertEqual(
            result["most_expensive_cost"],
            Decimal("40.00"),
        )

        self.assertEqual(
            result["potential_savings"],
            Decimal("20.00"),
        )

        self.assertEqual(
            result["savings_percentage"],
            Decimal("50.00"),
        )

    def test_cost_savings_when_no_suitable_box_exists(self):
        ShippingBox.objects.all().delete()

        result = get_cost_savings(self.order)

        self.assertEqual(result["suitable_boxes"], [])
        self.assertIsNone(result["potential_savings"])
        self.assertIsNone(result["savings_percentage"])
