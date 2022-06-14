#include "gmock/gmock.h"
#include "gtest/gtest.h"

// gmock code
testing::InSequence s;

// gtest code
TEST(helloworld, true)
{
    EXPECT_TRUE(false);
}
