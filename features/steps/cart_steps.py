from pages.storefront_page import StorefrontPage

@given(u'I am at the storefront')
def step_impl(context):
    context.storefront = StorefrontPage().visit_page(context)

@when(u'I search for {product}')
def step_impl(context, product):
    context.search_results = context.storefront\
        .search_for_product(context, product)

@when(u'I select the second result')
def step_impl(context):
    context.second_result_details_page = context.search_results\
        .select_result_number(context, '2')

@when(u'I change the selected variant')
def step_impl(context):
    context.select_variant_33 = context.second_result_details_page\
        .select_variant(context, '33')

@then(u'I can add the product to the Cart')
def step_impl(context):
    context.add_variant_to_cart = context.select_variant_33\
        .add_product_to_cart(context)\
        .verify_product_was_added_to_cart(context)
