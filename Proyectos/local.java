import java.util.Scanner;

public class MainClass {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Datos de la universidad y asignatura
        String carrera = "Ingeniería Industrial";
        String asignatura = "PROGRAMACION ESTRUCTURADA";
        String seccion = "0410";
        String profesor = "JOSE RAFAEL ROJAS";
        String periodo = "Septiembre - Diciembre 2023";

        // Cantidad de estudiantes y arreglo de notas
        int cantidadEstudiantes = obtenerCantidadEstudiantes(scanner);

        int[] asistencia = new int[cantidadEstudiantes];
        int[] practicas = new int[cantidadEstudiantes];
        int[] primerParcial = new int[cantidadEstudiantes];
        int[] examenFinal = new int[cantidadEstudiantes];
        char[] notasLiterales = new char[cantidadEstudiantes];

        // Ingreso de notas para cada estudiante
        for (int i = 0; i < cantidadEstudiantes; i++) {
            System.out.println("Ingrese las notas para el estudiante " + (i + 1) + ":");
            asistencia[i] = obtenerNota("Asistencia", scanner);
            practicas[i] = obtenerNota("Prácticas", scanner);
            primerParcial[i] = obtenerNota("Primer Parcial", scanner);
            examenFinal[i] = obtenerNota("Examen Final", scanner);

            // Calcular la nota final y la nota literal para este estudiante
            int notaFinal = calcularNotaFinal(asistencia[i], practicas[i], primerParcial[i], examenFinal[i]);
            notasLiterales[i] = calcularNotaLiteral(notaFinal);
        }

        // Imprimir resultados
        imprimirResultados(carrera, asignatura, seccion, profesor, periodo, asistencia, practicas, primerParcial, examenFinal, notasLiterales);
    }

    public static int obtenerCantidadEstudiantes(Scanner scanner) {
        int cantidadEstudiantes = 0;
        while (cantidadEstudiantes <= 0) {
            try {
                System.out.print("Ingrese la cantidad de estudiantes: ");
                cantidadEstudiantes = scanner.nextInt();
                if (cantidadEstudiantes <= 0) {
                    System.out.println("Por favor, ingrese un número de estudiantes válido.");
                }
            } catch (java.util.InputMismatchException e) {
                System.out.println("Por favor, ingrese un número entero válido.");
                scanner.next(); // Limpia el buffer del scanner
            }
        }
        return cantidadEstudiantes;
    }

    public static int obtenerNota(String nombreNota, Scanner scanner) {
        int nota = 0;
        while (nota < 0 || nota > 100) {
            try {
                System.out.print("Ingrese la nota de " + nombreNota + ": ");
                nota = scanner.nextInt();
                if (nota < 0 || nota > 100) {
                    System.out.println("Por favor, ingrese una nota válida entre 0 y 100.");
                }
            } catch (java.util.InputMismatchException e) {
                System.out.println("Por favor, ingrese un número entero válido.");
                scanner.next(); // Limpia el buffer del scanner
            }
        }
        return nota;
    }

    public static int calcularNotaFinal(int asistencia, int practicas, int primerParcial, int examenFinal) {
        return asistencia + practicas + primerParcial + examenFinal;
    }

    public static char calcularNotaLiteral(int notaFinal) {
        if (notaFinal >= 90) {
            return 'A';
        } else if (notaFinal >= 80) {
            return 'B';
        } else if (notaFinal >= 75) {
            return 'C';
        } else if (notaFinal >= 70) {
            return 'D';
        } else {
            return 'F';
        }
    }

    public static void imprimirResultados(String carrera, String asignatura, String seccion, String profesor, String periodo,
                                          int[] asistencia, int[] practicas, int[] primerParcial, int[] examenFinal, char[] notasLiterales) {
        System.out.println("****************************************************************************");
        System.out.println("UNIVERSIDAD DOMINICANA O&M");
        System.out.println("Departamento de Registro Académico");
        System.out.println("Reporte de Calificaciones");
        System.out.println("Periodo: " + periodo);
        System.out.println("****************************************************************************");
        System.out.println("Carrera.........: " + carrera);
        System.out.println("Asignatura......: " + asignatura);
        System.out.println("Sección.........: " + seccion);
        System.out.println("Profesor........: " + profesor);
        System.out.println("****************************************************************************");
        System.out.println("Matrícula  AS  PP  TP  EF  NOTA  NL");
        System.out.println("****************************************************************************");
        for (int i = 0; i < asistencia.length; i++) {
            System.out.printf("%-10d %-3d %-3d %-3d %-3d %-5d %c\n", i + 1, asistencia[i], practicas[i], primerParcial[i],
                    examenFinal[i], calcularNotaFinal(asistencia[i], practicas[i], primerParcial[i], examenFinal[i]),
                    notasLiterales[i]);
        }
        System.out.println("-------------------------------------------------------------------------------------");
        System.out.println("Cantidad de Estudiantes: " + asistencia.length);
        System.out.println("Nota Mayor: " + calcularNotaMayor(asistencia, practicas, primerParcial, examenFinal));
        System.out.println("Nota Menor: " + calcularNotaMenor(asistencia, practicas, primerParcial, examenFinal));
        System.out.printf("Nota Promedio: %.2f\n", calcularNotaPromedio(asistencia, practicas, primerParcial, examenFinal));
    }

    public static int calcularNotaMayor(int[] asistencia, int[] practicas, int[] primerParcial, int[] examenFinal) {
        int notaMayor = Integer.MIN_VALUE;
        for (int i = 0; i < asistencia.length; i++) {
            int notaFinal = calcularNotaFinal(asistencia[i], practicas[i], primerParcial[i], examenFinal[i]);
            if (notaFinal > notaMayor) {
                notaMayor = notaFinal;
            }
        }
        return notaMayor;
    }

    public static int calcularNotaMenor(int[] asistencia, int[] practicas, int[] primerParcial, int[] examenFinal) {
        int notaMenor = Integer.MAX_VALUE;
        for (int i = 0; i < asistencia.length; i++) {
            int notaFinal = calcularNotaFinal(asistencia[i], practicas[i], primerParcial[i], examenFinal[i]);
            if (notaFinal < notaMenor) {
                notaMenor = notaFinal;
            }
        }
        return notaMenor;
    }

    public static double calcularNotaPromedio(int[] asistencia, int[] practicas, int[] primerParcial, int[] examenFinal) {
        double suma = 0;
        for (int i = 0; i < asistencia.length; i++) {
            suma += calcularNotaFinal(asistencia[i], practicas[i], primerParcial[i], examenFinal[i]);
        }
        return suma / asistencia.length;
    }
}
