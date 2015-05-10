gcd' :: Integral a => a -> a -> a
gcd' a b 
    | b /= 0 = (gcd' b $ mod a b)
    | otherwise = a

prime :: Integral a => a -> Bool
prime x = primeLoop x $ x-1

primeLoop :: Integral a => a -> a -> Bool
primeLoop x 1 = True
primeLoop x d 
    | mod x d /= 0 = primeLoop x $ d-1
    | otherwise = False

lcm' :: Integral a => a -> a -> a
lcm' a b = abs a*b `div` gcd' a b

l = [10,11,12,13,14,15,16,17,18,19,20]

main = putStrLn . show $ filter prime l



-- main = putStrLn $ show $ lcm' 0 3


