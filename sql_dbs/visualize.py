import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def valid_input_file(path):
    if not os.path.isfile(path):
        msg = 'Provided path does not exist or is not a file.'
        raise argparse.ArgumentTypeError(msg)
    else:
        try:
            df = pd.read_csv(path)
        except Exception as e:
            print(e)
            raise argparse.ArgumentTypeError('Bad input file') from e

    return df


def label_format(v):
    return '{} (sec)'.format(v)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, type=valid_input_file,
                        help='File with input data')
    parser.add_argument('-o', '--out', default='./graphs',
                        help='Output folder for generated graphs. '
                             'If it doesn\'t exist, it will be created,')
    parser.add_argument('-x', '--independent-vars', nargs='+',
                        default=['x1', 'x2'],
                        help='Column names in the input file to be used as  '
                             'independent variables to build graphs '
                             '(2 values, space-separated).')
    parser.add_argument('-y', '--dependent-var', default='y1',
                        help='Column name in the input file to be used as '
                             'dependent variable to build graphs.')

    return parser.parse_args()


def create_linear_graphs(df, indep_names, dep_name, output_folder):
    """
    Groups dataset by each of two independent variables (thus, 'fixing' 1 variable)
    and plots a relation between other (non-fixed) independent variable
    and dependent one.
    Resulting graphs are saved into specified output directory.
    """
    sns.set()
    graph_number = 1
    for fixed_name in indep_names:
        other_name = [n for n in indep_names if n != fixed_name][0]
        fixed_values = df[fixed_name].unique()
        for value in fixed_values:
            group = df[df[fixed_name] == value].sort_values(other_name)

            plt.figure()
            plt.plot(other_name, dep_name, 'bo', data=group)
            plt.xlabel(other_name)
            plt.ylabel(label_format(dep_name))
            plt.title('{} = {}'.format(fixed_name, value))

            output_file = os.path.join(output_folder,
                                       'fixed-{}.png'.format(graph_number))
            plt.savefig(output_file)
            graph_number += 1


def create_heatmaps(df, indep_names, dep_name, output_folder):
    """
    Plots a relation between two independent variables and a dependent
    one in a heatmap.
    Resulting graphs are saved into specified output directory.
    """
    sns.set()
    target_columns = indep_names + [dep_name]
    x1, x2, y = target_columns
    df_heat = df[target_columns].sort_values(target_columns)
    # setup color palette
    colors_count = len(df_heat[dep_name].unique())
    palette = sns.cubehelix_palette(colors_count, start=2.5, rot=1., light=0.8)
    title = '{y}({x1},{x2})'.format(y=y, x1=x1, x2=x2)

    # 'pivot'ed heatmap
    pivot = df_heat.pivot(*target_columns)
    plt.figure()
    sns.heatmap(pivot, annot=True, cmap=palette)
    plt.xlabel(label_format(x2))
    plt.ylabel(label_format(x1))
    plt.title(title)
    plt.savefig(os.path.join(output_folder, 'heatmap-1.png'))

    # table-like heatmap
    plt.figure()
    df_heat = df_heat.rename(columns={x1: label_format(x1), x2: label_format(x2)})
    sns.heatmap(df_heat, yticklabels=False, annot=True, annot_kws={"size": 9},
                cmap=palette)
    plt.title(title)
    plt.savefig(os.path.join(output_folder, 'heatmap-2.png'))


def main():
    args = parse_args()
    df = args.file
    output_folder = args.out
    os.makedirs(output_folder, exist_ok=True)

    independent_var_names = args.independent_vars
    dependent_var_name = args.dependent_var

    create_linear_graphs(df, independent_var_names, dependent_var_name,
                         output_folder)
    create_heatmaps(df, independent_var_names, dependent_var_name,
                    output_folder)


if __name__ == '__main__':
    main()
