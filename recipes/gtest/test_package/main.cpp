#include "gmock/gmock.h"
#include "gtest/gtest.h"

// gtest code
TEST(helloworld, true)
{
    // gmock code
    testing::InSequence s;

    EXPECT_TRUE(true);
}
