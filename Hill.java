import java.util.Scanner;

public class Hill {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        System.out.println("|Enter 1 to Encrypt and 0 to Decrypt|");
        System.out.print("Enter a number : ");
        int choice = in.nextInt();
        in.nextLine();


        if(choice==1){
            System.out.print("Enter String to encrypt : ");
            String str = in.nextLine();
            System.out.print("enter key: ");
            String key = in.nextLine();
            System.out.print("String after encryption : ");
            System.out.println(encrypt(key.toLowerCase(),str.toLowerCase()));
        }
        else if(choice==0){
            System.out.println("enter String to decrypt: ");
            String str = in.nextLine();
            System.out.print("enter key: ");
            String key = in.nextLine();

            decrypt(str.toLowerCase(),key.toLowerCase());
        }
        else{
            System.out.println("enter a valid choice!");
        }
        System.out.println("=========================================================");
    }
    public static String encrypt(String key,String plainText){
        if(!isPerfectSquare(key.length())){
            return "enter a key whose length is a perfect square root.";
        }
        String ans = "";
        int root = (int)Math.sqrt(key.length());
        int k = 0;
        int[][] keyMat = new int[root][root];
        for (int i = 0; i < root; i++) {
            for (int j = 0; j < root; j++) {
                keyMat[i][j] = (key.charAt(k)-'a') % 26;
                k++;
            }
        }
        int lengthPlain = plainText.length();
        int[][] plainMat;
        if(root>=lengthPlain){
            for (int i = 0; i < root-lengthPlain; i++) {
                plainText += 'x';
                lengthPlain++;
            }
            plainMat = new int[root][1];
        } else{
            while(lengthPlain%root!=0){
                plainText += 'x';
                lengthPlain++;
            }
            plainMat = new int[root][lengthPlain/root];
        }
        int temp = 0;
        for (int i = 0; i < lengthPlain/root; i++) {
            for (int j = 0; j < root; j++) {
                plainMat[j][i] = (plainText.charAt(temp) -'a') % 26;
                temp++;
            }
        }

        char[][] finalMat = matrixMul(keyMat,plainMat);

        for (int i = 0; i < finalMat[0].length; i++) {
            for (int j = 0; j < finalMat.length; j++) {
                ans += finalMat[j][i];
            }
        }

//        for (int i = 0; i < root; i++) {
//            System.out.println(Arrays.toString(keyMat[i]));
//        }
//        System.out.println("=============================");
//        for (int i = 0; i < root; i++) {
//            System.out.println(Arrays.toString(plainMat[i]));
//        }
        return ans;
    }

    public static char[][] matrixMul(int[][] keyMat, int[][] plainMat) {
        char finalMat[][] = new char[keyMat.length][plainMat[0].length];
        for (int i = 0; i < finalMat.length; i++) {
            for (int j = 0; j < finalMat[i].length; j++) {
                for (int k = 0; k < keyMat[0].length; k++) {
                    finalMat[i][j] += (keyMat[i][k] * plainMat[k][j]) ;
                }
                finalMat[i][j] = (char)((finalMat[i][j] %26) + 97) ;
            }
        }
//        for (int i = 0; i < finalMat.length; i++) {
//            System.out.println(Arrays.toString(finalMat[i]));
//        }
//        System.out.println("==============================");
        return finalMat;
    }
    public static boolean isPerfectSquare(int a){
        int root = (int)Math.sqrt(a);
        return root*root == a;
    }
    public static int[][] calculateAdjoint(int[][] matrix) {
        int size = matrix.length;
        int[][] adjoint = new int[size][size];

        if (size == 1) {
            adjoint[0][0] = 1;
        } else if (size == 2) {
            adjoint[0][0] = matrix[1][1];
            adjoint[0][1] = -matrix[0][1];
            adjoint[1][0] = -matrix[1][0];
            adjoint[1][1] = matrix[0][0];
        } else {
            for (int i = 0; i < size; i++) {
                for (int j = 0; j < size; j++) {
                    int[][] submatrix = getSubmatrix(matrix, i, j);
                    adjoint[i][j] = (int) Math.pow(-1, i + j) * calculateDeterminant(submatrix);
                }
            }
            adjoint = transposeMatrix(adjoint);
        }

        return adjoint;
    }

    public static int[][] getSubmatrix(int[][] matrix, int rowToRemove, int colToRemove) {
        int size = matrix.length;
        int[][] submatrix = new int[size - 1][size - 1];
        int rowIndex = 0;
        int colIndex;

        for (int i = 0; i < size; i++) {
            if (i == rowToRemove) {
                continue;
            }

            colIndex = 0;
            for (int j = 0; j < size; j++) {
                if (j == colToRemove) {
                    continue;
                }

                submatrix[rowIndex][colIndex] = matrix[i][j];
                colIndex++;
            }
            rowIndex++;
        }

        return submatrix;
    }

    public static int calculateDeterminant(int[][] matrix) {
        int size = matrix.length;

        if (size == 2) {
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
        }

        int determinant = 0;
        for (int i = 0; i < size; i++) {
            determinant += matrix[0][i] * (int) Math.pow(-1, i) * calculateDeterminant(getSubmatrix(matrix, 0, i));
        }

        return determinant;
    }

    public static int[][] transposeMatrix(int[][] matrix) {
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[][] transposed = new int[cols][rows];

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                transposed[j][i] = matrix[i][j];
            }
        }

        return transposed;
    }
    /*--------------------------------------------------------------------------------*/

    // finding the modulo inverse of number A under modulo 'M'
    public static int modInverse(int A, int M) {
        for (int i = 1; i < M; i++) {
            if (((A % M) * (i % M)) % M == 1) {
                return i;
            }
        }
        return -1;
    }
    

    public static int[][] inverseOfKeyMatrix(int[][] keyMatrix) {
        int determinant = calculateDeterminant(keyMatrix);
        if (determinant < 0) {
            determinant = 26 - (Math.abs(determinant) % 26);
        }
        determinant = determinant % 26;
        int modularInverse = modInverse(determinant, 26);

        int[][] inverseMatrix = calculateAdjoint(keyMatrix);

        for (int i = 0; i < inverseMatrix.length; i++) {
            for (int j = 0; j < inverseMatrix[0].length; j++) {
                inverseMatrix[i][j] = (inverseMatrix[i][j]) % 26;
                if (inverseMatrix[i][j] < 0) {
                    inverseMatrix[i][j] = 26 - Math.abs(inverseMatrix[i][j]);
                }
                inverseMatrix[i][j] = (inverseMatrix[i][j] * modularInverse) % 26;
            }
        }
        return inverseMatrix;
    }
    public static void decrypt(String str,String key){
        if(!isPerfectSquare(key.length())){
            System.out.println("enter a key whose length is a perfect square root.");
        }
        int root = (int)Math.sqrt(key.length());
        int[][] keyMat = new int[root][root];
        int k=0;
        for (int i = 0; i < root; i++) {
            for (int j = 0; j < root; j++) {
                keyMat[i][j] = (key.charAt(k)-'a') % 26;
                k++;
            }
        }
        int temp =0;
        int[][] inverseKey = inverseOfKeyMatrix(keyMat);
        int[][] strMat = new int[root][str.length()/root];
        for (int i = 0; i < strMat[0].length; i++) {
            for (int j = 0; j < strMat.length; j++) {
                strMat[j][i] = (str.charAt(temp)-'a') % 26;
                temp++;
            }
        }

        char[][] finalText = matrixMul(inverseKey,strMat);

        String ans = "";
        for (int i = 0; i < finalText[0].length; i++) {
            for (int j = 0; j < finalText.length; j++) {
                ans += finalText[j][i];
            }
        }
        System.out.println("Plaintext : " + ans);
    }
}