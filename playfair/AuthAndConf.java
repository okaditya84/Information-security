import java.math.BigInteger;
import java.util.Random;

public class AuthAndConf {
    public static BigInteger[] select_prime_number() {
        Random rand = new Random();
        BigInteger[] prime_number = new BigInteger[2];
        int max_attempts = 1000;
        int count = 0;
        while (count < 2 && max_attempts > 0) {
            BigInteger randNumber = new BigInteger(256, rand);
            if (randNumber.isProbablePrime(100)) {
                prime_number[count] = randNumber;
                count++;
            }
            max_attempts--;
        }
        return prime_number;
    }

    public static BigInteger calculate_n(BigInteger[] prime_number) {
        return prime_number[0].multiply(prime_number[1]);
    }

    public static BigInteger calculate_fi_n(BigInteger[] prime_numbers) {
        BigInteger p1 = prime_numbers[0].subtract(BigInteger.ONE);
        BigInteger p2 = prime_numbers[1].subtract(BigInteger.ONE);
        return p1.multiply(p2);
    }

    public static boolean calculate_gcd(BigInteger e, BigInteger fi_n) {
        BigInteger temp;
        while (!fi_n.mod(e).equals(BigInteger.ZERO)) {
            temp = fi_n.mod(e);
            fi_n = e;
            e = temp;
        }
        return e.equals(BigInteger.ONE);
    }

    public static BigInteger find_e(BigInteger fi_n) {
        BigInteger e = BigInteger.TWO;
        while (e.compareTo(fi_n) < 0) {
            boolean for_e = calculate_gcd(e, fi_n);
            if (for_e) {
                return e;
            } else {
                e = e.add(BigInteger.ONE);
            }
        }
        return e;
    }

    public static BigInteger find_d(BigInteger a, BigInteger m) {
        BigInteger m0 = m;
        BigInteger x0 = BigInteger.ZERO;
        BigInteger x1 = BigInteger.ONE;

        while (a.compareTo(BigInteger.ONE) > 0) {
            BigInteger q = a.divide(m);
            BigInteger t = m;

            m = a.mod(m);
            a = t;

            t = x0;
            x0 = x1.subtract(q.multiply(x0));
            x1 = t;
        }

        if (x1.compareTo(BigInteger.ZERO) < 0) {
            x1 = x1.add(m0);
        }

        return x1;
    }

    public static void main(String[] args) {

        BigInteger[] prime_a = select_prime_number();
        BigInteger[] prime_b = select_prime_number();
        System.out.println("prime " + prime_a[0] + " " + prime_a[1]);

        BigInteger n_a = calculate_n(prime_a);
        BigInteger n_b = calculate_n(prime_b);

        // System.out.println("n: " + n_a + " " + n_b);

        BigInteger fi_n_a = calculate_fi_n(prime_a);
        BigInteger fi_n_b = calculate_fi_n(prime_b);
        // System.out.println("fi: " + fi_n_a + " " + fi_n_b);

        BigInteger e_a = find_e(fi_n_a);
        BigInteger e_b = find_e(fi_n_b);

        // System.out.println("e: " + e_a + " " + e_b);

        BigInteger d_a = find_d(e_a, fi_n_a);
        BigInteger d_b = find_d(e_b, fi_n_b);

        // System.out.println("d: " + d_a + " " + d_b);

        BigInteger x = BigInteger.valueOf(5);
        BigInteger y = x.modPow(e_a, n_a);
        BigInteger z = y.modPow(e_b, n_b);

        System.out.println("y: " + y);
        System.out.println("z: " + z);

        BigInteger y_det = z.modPow(d_b, n_b);
        BigInteger x_det = y_det.modPow(d_a, n_a);

        System.out.println("y_det: " + y_det);
        System.out.println("x_det: " + x_det);

        if (x.equals(x_det)) {
            System.out.println("Decryption successful. x matches x_det.");
        } else {
            System.out.println("Decryption failed. x does not match x_det.");
        }
    }
}
